from __init__ import client_stepfunctions, client_lambda
from botocore.exceptions import ClientError
import json

def test_invoke_lambda_function_directly():
    # Prepare the input for the Lambda function
    lambda_input = {
        "url": "https://jsonplaceholder.typicode.com/posts/1",
        "method": "GET",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": None
    }

    try:
        # Invoke the Lambda function directly
        response = client_lambda.invoke(
            FunctionName='ApiCallFunction',
            InvocationType='RequestResponse',
            Payload=json.dumps(lambda_input)
        )
        
        # Read and parse the response
        response_payload = json.loads(response['Payload'].read().decode('utf-8'))
        
        # Assert the status code and other details
        assert response_payload['statusCode'] == 200, f"Expected status code 200, got {response_payload['statusCode']}"
        assert 'userId' in json.loads(response_payload['body']), "Response body does not contain expected data"
        
        print("Test passed: Lambda function invoked directly and returned expected results.")
    except ClientError as e:
        print(f"Test failed: {e}")


def test_invoke_lambda_through_step_functions():
    # Prepare the input for the Step Functions state machine
    state_machine_input = {
        "template_name": "GetUser",
        "params": {
            "url_params": ["1"],  # Example URL param for the API
            "header_params": ["Bearer dummy_token"],  # Example header param
            "body_params": []  # No body in this example
        }
    }

    try:
        # Start the Step Functions state machine execution
        response = client_stepfunctions.start_execution(
            stateMachineArn='arn:aws:states:us-east-1:000000000000:stateMachine:APICallStateMachine',
            input=json.dumps(state_machine_input)
        )

        # Wait for the execution to complete
        execution_arn = response['executionArn']
        execution_status = client_stepfunctions.describe_execution(executionArn=execution_arn)
        
        # Poll for the status of the execution until it finishes
        while execution_status['status'] in ['RUNNING']:
            execution_status = client_stepfunctions.describe_execution(executionArn=execution_arn)

        # Assert the execution result
        assert execution_status['status'] == 'SUCCEEDED', f"Expected status SUCCEEDED, got {execution_status['status']}"
        
        execution_output = json.loads(execution_status['output'])
        assert 'statusCode' in execution_output['api_response']['Payload'], "Lambda function response missing statusCode"
        assert execution_output['api_response']['Payload']['statusCode'] == 200, f"Expected status code 200, got {execution_output['api_response']['Payload']['statusCode']}"

        print("Test passed: Step Functions invoked Lambda function successfully and returned expected results.")
    except ClientError as e:
        print(f"Test failed: {e}")

test_invoke_lambda_function_directly()
test_invoke_lambda_through_step_functions()
