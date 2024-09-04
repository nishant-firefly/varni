import json
import boto3

# Initialize SQS client
sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')

# Define SQS queue URL
queue_url = 'http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/fileQueue'

# Create a JSON payload
message = {
    'type': 'notification',
    'content': {
        'title': 'Test Notification',
        'body': 'This is a JSON payload message.'
    }
}

# Send the JSON payload message
response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=json.dumps(message)
)

print(f"Message ID: {response['MessageId']}")
