import boto3

# Initialize SQS client
sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')

# Define SQS queue URL
queue_url = 'http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/fileQueue'

# Create a large message payload
large_message = 'A' * 256000  # SQS message size limit is 256 KB

# Send the large message
response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=large_message
)

print(f"Message ID: {response['MessageId']}")
