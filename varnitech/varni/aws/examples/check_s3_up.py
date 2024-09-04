import boto3
from botocore.exceptions import EndpointConnectionError, ClientError
import os
from botocore.exceptions import NoRegionError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=".env")

# Get LocalStack endpoints from environment variables
localstack_endpoint = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
s3_endpoint = os.getenv("S3_ENDPOINT", f"{localstack_endpoint}/s3")
sqs_endpoint = os.getenv("SQS_ENDPOINT", f"{localstack_endpoint}/sqs")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

# Specify AWS region (LocalStack does not require an actual region, but we specify 'us-east-1' for boto3 compatibility)
aws_region = 'us-east-1'

# Initialize AWS clients with LocalStack endpoints, region, and credentials
s3_client = boto3.client('s3', endpoint_url=s3_endpoint,
                         aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key,
                         region_name=aws_region)

iam_client = boto3.client('iam', endpoint_url=s3_endpoint,
                         aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key,
                         region_name=aws_region)

def check_s3_service_and_iam():

    try:
        # Check if S3 service is available by listing buckets (if any)
        # Perform an operation that verifies S3 service availability
        try:
            response = s3_client.list_buckets()
            print("S3 service is up and reachable.")

        except EndpointConnectionError as e:
            print(f"Error: Unable to connect to S3 service at {s3_endpoint}.")
            print(e)

        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucket':
                print("ClientError: NoSuchBucket - This error should not occur for list_buckets() operation.")
            else:
                print(f"ClientError: {e}")

        except Exception as e:
            print(f"Error: {e}")
        """
        # Retrieve IAM policies
        try:
            response = iam_client.list_policies()
            if 'Policies' in response:
                print("IAM policies available:")
                for policy in response['Policies']:
                    print(f"- {policy['PolicyName']}")
            else:
                print("No IAM policies found.")
        except Exception as e:
            print(f"Error retrieving IAM policies: {e}")
        """

    except EndpointConnectionError as e:
        # Handle connection error
        print(f"Error: Unable to connect to services at {endpoint_url}.")
        print(e)

if __name__ == "__main__":
    check_s3_service_and_iam()

