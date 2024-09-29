import boto3
from botocore.exceptions import ClientError

# Initialize the Lambda client for LocalStack
lambda_client = boto3.client(
    'lambda',
    endpoint_url='http://localhost:4566',  # Ensure no extra path like '/lambda'
    region_name='us-east-1',                # Use your desired region
    aws_access_key_id='test',                # Dummy credentials for LocalStack
    aws_secret_access_key='test'
)

# Create a simple Lambda function
try:
    with open('function.zip', 'rb') as f:
        zipped_code = f.read()

    response = lambda_client.create_function(
        FunctionName='my_lambda_function',
        Runtime='python3.8',
        Role='arn:aws:iam::000000000000:role/execution_role',  # Dummy role ARN
        Handler='lambda_function.lambda_handler',
        Code={'ZipFile': zipped_code},
        Publish=True
    )
    print("Function created:", response)
except ClientError as e:
    print("Error creating Lambda function:", e)

# Invoke the Lambda function
try:
    response = lambda_client.invoke(
        FunctionName='my_lambda_function',
        Payload=b'{}'
    )
    payload = response['Payload'].read().decode()
    print("Function invoked, response:", payload)
except ClientError as e:
    print("Error invoking Lambda function:", e)
