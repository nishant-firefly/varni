import os
import boto3
from botocore.exceptions import NoRegionError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=".env")

# Get LocalStack endpoints from environment variables
localstack_endpoint = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
sqs_endpoint = os.getenv("SQS_ENDPOINT", f"{localstack_endpoint}/sqs")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

# Specify AWS region (LocalStack does not require an actual region, but we specify 'us-east-1' for boto3 compatibility)
aws_region = 'us-east-1'

# Initialize AWS clients with LocalStack endpoints, region, and credentials
sqs_client = boto3.client('sqs', endpoint_url=sqs_endpoint,
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=aws_region)

def is_service_up(endpoint):
    try:
        # Attempt a basic operation to verify service availability
        response = sqs_client.list_queues()
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error connecting to {endpoint}: {e}")
        return False

# Check if SQS service is running
def check_sqs_service():
    try:
        if is_service_up(sqs_endpoint):
            print("SQS service is running.")
        else:
            print("SQS service is not reachable.")
    except NoRegionError:
        print("No region specified.")

# Example usage
if __name__ == "__main__":
    check_sqs_service()
