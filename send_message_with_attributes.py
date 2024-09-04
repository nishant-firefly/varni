import boto3

# Initialize SQS client
sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')

# Define SQS queue URL
queue_url = 'http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/fileQueue'

# Send a message with attributes
response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody='This message has attributes.',
    MessageAttributes={
        'Author': {
            'StringValue': 'Deepti',
            'DataType': 'String'
        },
        'Priority': {
            'StringValue': 'High',
            'DataType': 'String'
        }
    }
)

print(f"Message ID: {response['MessageId']}")
