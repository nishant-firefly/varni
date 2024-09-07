import boto3
import json
import os

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
        if os.path.exists("lambda_function.zip"):
            with open("lambda_function.zip", "rb") as f:
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
        if os.path.exists("step_function.json"):
            with open("step_function.json", "r") as f:
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
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_resources()
