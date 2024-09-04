import boto3

def view_sqs_and_sns():
    # Create SQS and SNS clients
    sqs = boto3.client('sqs', endpoint_url='http://localhost.localstack.cloud:4566')
    sns = boto3.client('sns', endpoint_url='http://localhost.localstack.cloud:4566')

    # List SQS queues
    queues = sqs.list_queues()
    print("SQS Queues:")
    for url in queues.get('QueueUrls', []):
        print(f" - {url}")

    # List SNS topics
    topics = sns.list_topics()
    print("SNS Topics:")
    for topic in topics.get('Topics', []):
        print(f" - {topic['TopicArn']}")

if __name__ == "__main__":
    view_sqs_and_sns()
