from fastapi import APIRouter
import boto3
import json

router = APIRouter()

# Initialize AWS clients with region_name
sqs = boto3.client('sqs', endpoint_url="http://localstack:4566", region_name="us-east-1")
sns = boto3.client('sns', endpoint_url="http://localstack:4566", region_name="us-east-1")
stepfunctions = boto3.client('stepfunctions', endpoint_url="http://localstack:4566", region_name="us-east-1")
s3 = boto3.client('s3', endpoint_url="http://localstack:4566", region_name="us-east-1")

@router.post("/invoke-step-function/")
async def invoke_step_function():
    response = stepfunctions.start_execution(
        stateMachineArn='arn:aws:states:us-east-1:123456789012:stateMachine:MyStateMachine',
        input=json.dumps({"message": "Hello from FastAPI"})
    )
    return {"status": "Step Function invoked", "executionArn": response['executionArn']}

@router.get("/list-s3-objects/")
async def list_s3_objects():
    bucket_name = 'my-localstack-bucket'
    response = s3.list_objects_v2(Bucket=bucket_name)
    
    if 'Contents' in response:
        objects = [obj['Key'] for obj in response['Contents']]
    else:
        objects = []
    
    return {"bucket": bucket_name, "objects": objects}
