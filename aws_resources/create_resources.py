# import boto3
# import json
# import os

# # Initialize LocalStack resources
# localstack_endpoint = "http://localhost:4566"

# # Ensure you set the credentials explicitly if needed
# session = boto3.Session(
#     aws_access_key_id='test',
#     aws_secret_access_key='test',
#     region_name='us-east-1'
# )

# sqs = session.client('sqs', endpoint_url=localstack_endpoint)
# sns = session.client('sns', endpoint_url=localstack_endpoint)
# lambda_client = session.client('lambda', endpoint_url=localstack_endpoint)
# iam_client = session.client('iam', endpoint_url=localstack_endpoint)
# stepfunctions = session.client('stepfunctions', endpoint_url=localstack_endpoint)
# s3 = session.client('s3', endpoint_url=localstack_endpoint)

# def create_resources():
#     try:
#         # Create IAM Role for Lambda execution
#         assume_role_policy = {
#             "Version": "2012-10-17",
#             "Statement": [
#                 {
#                     "Effect": "Allow",
#                     "Principal": {
#                         "Service": "lambda.amazonaws.com"
#                     },
#                     "Action": "sts:AssumeRole"
#                 }
#             ]
#         }

#         role_name = "LambdaExecutionRole"
#         try:
#             role = iam_client.create_role(
#                 RoleName=role_name,
#                 AssumeRolePolicyDocument=json.dumps(assume_role_policy),
#                 Description="Role to allow Lambda execution"
#             )
#         except iam_client.exceptions.EntityAlreadyExistsException:
#             print("IAM Role already exists.")
#             role = iam_client.get_role(RoleName=role_name)
        
#         # Attach policy to allow Lambda access to logs and S3
#         iam_client.attach_role_policy(
#             RoleName=role_name,
#             PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
#         )
        
#         iam_client.attach_role_policy(
#             RoleName=role_name,
#             PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
#         )

#         # Create Lambda function with the IAM role
#         if os.path.exists("lambda_function.zip"):
#             with open("lambda_function.zip", "rb") as f:
#                 try:
#                     lambda_client.create_function(
#                         FunctionName="MyLambda",
#                         Runtime="python3.8",
#                         Role=role['Role']['Arn'],
#                         Handler="lambda_function.lambda_handler",
#                         Code={'ZipFile': f.read()},
#                         Timeout=300,
#                     )
#                 except lambda_client.exceptions.ResourceConflictException:
#                     print("Lambda function already exists.")
#         else:
#             print("Lambda function zip file not found.")

#         # Create S3 Bucket
#         try:
#             s3.create_bucket(Bucket='my-localstack-bucket')
#         except s3.exceptions.BucketAlreadyExists:
#             print("S3 Bucket already exists.")
        
#         # Create Step Function State Machine
#         if os.path.exists("step_function.json"):
#             with open("step_function.json", "r") as f:
#                 step_function_definition = json.load(f)

#             try:
#                 stepfunctions.create_state_machine(
#                     name='MyStateMachine',
#                     definition=json.dumps(step_function_definition),
#                     roleArn=role['Role']['Arn']
#                 )
#             except stepfunctions.exceptions.StateMachineAlreadyExists:
#                 print("Step Function State Machine already exists.")
#         else:
#             print("Step function JSON file not found.")

#         print("Resources created: IAM, Lambda, S3, and Step Functions.")
    
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     create_resources()







import boto3
import json
import os
import time

# Initialize LocalStack resources
localstack_endpoint = "http://localhost:4566"

# Ensure you set the credentials explicitly if needed
session = boto3.Session(
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

sqs = session.client('sqs', endpoint_url=localstack_endpoint)
sns = session.client('sns', endpoint_url=localstack_endpoint)
lambda_client = session.client('lambda', endpoint_url=localstack_endpoint)
iam_client = session.client('iam', endpoint_url=localstack_endpoint)
stepfunctions = session.client('stepfunctions', endpoint_url=localstack_endpoint)
s3 = session.client('s3', endpoint_url=localstack_endpoint)

def create_resources():
    try:
        # Define file paths
        lambda_zip_path = "D:/aws_local_project/aws_resources/lambda_function.zip"
        step_function_json_path = "D:/aws_local_project/aws_resources/step_function.json"

        # Logging file paths
        print(f"Checking if {lambda_zip_path} exists.")
        print(f"Checking if {step_function_json_path} exists.")

        # Create IAM Role for Lambda execution
        assume_role_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }

        role_name = "LambdaExecutionRole"
        try:
            role = iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(assume_role_policy),
                Description="Role to allow Lambda execution"
            )
        except iam_client.exceptions.EntityAlreadyExistsException:
            print("IAM Role already exists.")
            role = iam_client.get_role(RoleName=role_name)
        
        # Attach policy to allow Lambda access to logs and S3
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
        )
        
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
        )

        # Create Lambda function with the IAM role
        if os.path.exists(lambda_zip_path):
            with open(lambda_zip_path, "rb") as f:
                try:
                    lambda_client.create_function(
                        FunctionName="MyLambda",
                        Runtime="python3.8",
                        Role=role['Role']['Arn'],
                        Handler="lambda_function.lambda_handler",
                        Code={'ZipFile': f.read()},
                        Timeout=300,
                    )
                except lambda_client.exceptions.ResourceConflictException:
                    print("Lambda function already exists.")
        else:
            print("Lambda function zip file not found.")

        # Create S3 Bucket
        try:
            s3.create_bucket(Bucket='my-localstack-bucket')
        except s3.exceptions.BucketAlreadyExists:
            print("S3 Bucket already exists.")
        
        # Create Step Function State Machine
        if os.path.exists(step_function_json_path):
            with open(step_function_json_path, "r") as f:
                step_function_definition = json.load(f)

            try:
                stepfunctions.create_state_machine(
                    name='MyStateMachine',
                    definition=json.dumps(step_function_definition),
                    roleArn=role['Role']['Arn']
                )
            except stepfunctions.exceptions.StateMachineAlreadyExists:
                print("Step Function State Machine already exists.")
        else:
            print("Step function JSON file not found.")

        print("Resources created: IAM, Lambda, S3, and Step Functions.")

        # List Lambda functions
        response = lambda_client.list_functions()
        print("Lambda Functions:")
        print(response)

        # List Step Functions state machines
        response = stepfunctions.list_state_machines()
        print("Step Functions State Machines:")
        print(response)

        # Invoke Lambda function
        try:
            response = lambda_client.invoke(
                FunctionName="MyLambda",
                InvocationType="RequestResponse",
                Payload=json.dumps({"key": "value"})
            )
            print("Lambda Function Invocation Response:")
            print(response['Payload'].read().decode('utf-8'))
        except lambda_client.exceptions.ResourceNotFoundException:
            print("Lambda function does not exist.")
        
        # Start Step Function Execution
        def start_step_function_execution():
            try:
                response = stepfunctions.start_execution(
                    stateMachineArn='arn:aws:states:us-east-1:000000000000:stateMachine:MyStateMachine',
                    input=json.dumps({"input_key": "input_value"})
                )
                return response['executionArn']
            except Exception as e:
                print(f"Failed to start Step Function execution: {e}")
                return None

        # Get Step Function Execution Status
        def get_execution_status(execution_arn):
            try:
                while True:
                    response = stepfunctions.describe_execution(executionArn=execution_arn)
                    status = response['status']
                    print(f"Execution ARN: {execution_arn}, Status: {status}")
                    if status in ['SUCCEEDED', 'FAILED', 'TIMED_OUT', 'ABORTED']:
                        break
                    time.sleep(5)  # Poll every 5 seconds
            except Exception as e:
                print(f"Failed to get Step Function execution status: {e}")

        # Execute Step Function and check status
        execution_arn = start_step_function_execution()
        if execution_arn:
            get_execution_status(execution_arn)
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_resources()
