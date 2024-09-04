import boto3

sqs = boto3.client('sqs', endpoint_url='http://localhost.localstack.cloud:4566')
sns = boto3.client('sns', endpoint_url='http://localhost.localstack.cloud:4566')

# Create SQS queue
queue_response = sqs.create_queue(QueueName='fileQueue')
print("SQS Queue URL:", queue_response['QueueUrl'])

# Create SNS topic
topic_response = sns.create_topic(Name='fileTopic')
print("SNS Topic ARN:", topic_response['TopicArn'])
