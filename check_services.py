import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_lambda_service():
    """Check the status of the Lambda service."""
    client = boto3.client('lambda', endpoint_url=os.getenv('LOCALSTACK_ENDPOINT'),
                          aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                          region_name=os.getenv('REGION_NAME'))
    
    try:
        response = client.list_functions()
        print("Lambda service is running.")
        print(response)
    except Exception as e:
        print("Lambda service is not reachable.")
        print(e)

if __name__ == "__main__":
    check_lambda_service()
