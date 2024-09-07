# import json
# import boto3

# def lambda_handler(event, context):
#     s3 = boto3.client('s3')
#     bucket_name = 'my-localstack-bucket'
    
#     # List objects in the bucket
#     response = s3.list_objects_v2(Bucket=bucket_name)
    
#     if 'Contents' in response:
#         objects = [obj['Key'] for obj in response['Contents']]
#     else:
#         objects = []

#     return {
#         'statusCode': 200,
#         'body': json.dumps(f'Objects in bucket {bucket_name}: {objects}')
#     }


import json
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'my-localstack-bucket'
    
    try:
        # List objects in the bucket
        response = s3.list_objects_v2(Bucket=bucket_name)
        
        if 'Contents' in response:
            objects = [obj['Key'] for obj in response['Contents']]
        else:
            objects = []

        logger.info(f'Objects in bucket {bucket_name}: {objects}')
        return {
            'statusCode': 200,
            'body': json.dumps(f'Objects in bucket {bucket_name}: {objects}')
        }
    except ClientError as e:
        logger.error(f'Error: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
