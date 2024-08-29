import boto3
import zipfile
import os

def create_zip():
    """Create a ZIP file of the Lambda function."""
    with zipfile.ZipFile('lambda_function.zip', 'w') as z:
        for root, dirs, files in os.walk('lambda_function'):
            for file in files:
                z.write(os.path.join(root, file),
                        os.path.relpath(os.path.join(root, file),
                                        os.path.join('lambda_function', '..')))

def deploy_lambda():
    """Deploy the Lambda function to LocalStack."""
    # Initialize Boto3 client for Lambda
    client = boto3.client('lambda', endpoint_url='http://localhost:4566',
                          aws_access_key_id='test',
                          aws_secret_access_key='test',
                          region_name='us-east-1')
    
    # Create ZIP file of the Lambda function
    create_zip()
    
    with open('lambda_function.zip', 'rb') as f:
        zipped_code = f.read()
    
    # Create Lambda function
    response = client.create_function(
        FunctionName='my_lambda_function',
        Runtime='python3.8',
        Role='arn:aws:iam::000000000000:role/lambda-role',
        Handler='handler.lambda_handler',
        Code=dict(ZipFile=zipped_code),
        Timeout=300,
    )
    
    print("Lambda function deployed:")
    print(response)

if __name__ == "__main__":
    deploy_lambda()
