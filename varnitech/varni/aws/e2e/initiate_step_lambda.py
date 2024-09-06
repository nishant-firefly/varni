from __init__ import client_stepfunctions, client_lambda
import json
import os
import zipfile
from botocore.exceptions import ClientError

# Lambda function code
lambda_function_code = '''
import json
import requests

def lambda_handler(event, context):
    url = event['url']
    method = event['method']
    headers = event.get('headers', {})
    body = event.get('body', None)

    try:
        response = requests.request(method, url, headers=headers, data=body)
        return {
            'statusCode': response.status_code,
            'body': response.text
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
'''

def create_lambda_zip(zip_file_name, file_name, function_code):
    with open(file_name, 'w') as f:
        f.write(function_code)
    with zipfile.ZipFile(zip_file_name, 'w') as z:
        z.write(file_name)
    os.remove(file_name)

def delete_lambda_function_if_exists(function_name):
    try:
        response = client_lambda.get_function(FunctionName=function_name)
        if 'Configuration' in response:
            client_lambda.delete_function(FunctionName=function_name)
            print(f"Deleted existing Lambda function: {function_name}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Lambda function {function_name} does not exist. Proceeding to create.")
        else:
            print(f"Error deleting Lambda function: {e}")

def deploy_lambda_function():
    zip_file_name = 'function.zip'
    file_name = 'lambda_function.py'
    function_name = 'ApiCallFunction'
    
    # Create a ZIP file of the Lambda function
    create_lambda_zip(zip_file_name, file_name, lambda_function_code)
    
    # Delete the function if it already exists to avoid update issues
    delete_lambda_function_if_exists(function_name)
    
    # Create the Lambda function
    try:
        with open(zip_file_name, 'rb') as f:
            zipped_code = f.read()

        response = client_lambda.create_function(
            FunctionName=function_name,
            Runtime='python3.8',
            Role='arn:aws:iam::000000000000:role/lambda-role',  # Use a dummy ARN for LocalStack
            Handler='lambda_function.lambda_handler',
            Code=dict(ZipFile=zipped_code),
            Timeout=300,
            MemorySize=128,
            Publish=True
        )
        print(f"Lambda function created with ARN: {response['FunctionArn']}")
    except ClientError as e:
        print(f"Error creating Lambda function: {e}")
    finally:
        os.remove(zip_file_name)

state_machine_definition = {
  "Comment": "Step Function to retrieve API template, execute API call via Lambda, and store result.",
  "StartAt": "GetTemplateFromDynamoDB",
  "States": {
    "GetTemplateFromDynamoDB": {
      "Type": "Task",
      "Resource": "arn:aws:states:::dynamodb:getItem",
      "Parameters": {
        "TableName": "ApiTemplates",
        "Key": {
          "TemplateName": {
            "S.$": "$.template_name"
          }
        }
      },
      "ResultPath": "$.api_template",
      "Next": "ReplacePlaceholders"
    },
    "ReplacePlaceholders": {
      "Type": "Pass",
      "ResultPath": "$.final_api_details",
      "Parameters": {
        "url": "$.api_template.Item.TemplateUrl.S",
        "method": "$.api_template.Item.HttpMethod.S",
        "headers": "$.api_template.Item.Headers.M",
        "body": "$.api_template.Item.BodyTemplate.S"
      },
      "Next": "CallLambda"
    },
    "CallLambda": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": {
        "FunctionName": "ApiCallFunction",
        "Payload": {
          "url.$": "$.final_api_details.url",
          "method.$": "$.final_api_details.method",
          "headers.$": "$.final_api_details.headers",
          "body.$": "$.final_api_details.body"
        }
      },
      "ResultPath": "$.api_response",
      "Next": "StoreResultInDynamoDB"
    },
    "StoreResultInDynamoDB": {
      "Type": "Task",
      "Resource": "arn:aws:states:::dynamodb:putItem",
      "Parameters": {
        "TableName": "ApiExecutionResults",
        "Item": {
          "TemplateName": {
            "S.$": "$.template_name"
          },
          "ExecutionResult": {
            "M": {
              "status_code": {
                "N.$": "$.api_response.Payload.statusCode"
              },
              "response_body": {
                "S.$": "$.api_response.Payload.body"
              }
            }
          }
        }
      },
      "End": True
    }
  }
}

def delete_state_machine_if_exists(state_machine_name):
    try:
        response = client_stepfunctions.list_state_machines()
        for sm in response['stateMachines']:
            if sm['name'] == state_machine_name:
                client_stepfunctions.delete_state_machine(stateMachineArn=sm['stateMachineArn'])
                print(f"Deleted existing state machine: {state_machine_name}")
                break
    except ClientError as e:
        print(f"Error deleting state machine: {e}")

def one_time_initiate_state_machine():
    state_machine_name = 'APICallStateMachine'
    
    # Delete the state machine if it already exists
    delete_state_machine_if_exists(state_machine_name)
    
    # Create the new state machine
    response = client_stepfunctions.create_state_machine(
        name=state_machine_name,
        definition=json.dumps(state_machine_definition),
        roleArn='arn:aws:iam::123456789012:role/DummyRole'  # Replace with your IAM role
    )
    print(f"State machine created with ARN: {response['stateMachineArn']}")

def initiate_lambda_step():
  # Deploy Lambda function and create State Machine
  deploy_lambda_function()
  one_time_initiate_state_machine()
