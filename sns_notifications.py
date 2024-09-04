import boto3
import requests

def sns_notifications():
    session = boto3.Session()
    sns = session.client('sns', endpoint_url='http://localhost:4566')

    topic_arn = 'arn:aws:sns:us-east-1:000000000000:fileTopic'  # Replace with your topic ARN

    def lambda_handler(event, context):
        message = event['Records'][0]['Sns']['Message']
        print(f"Received message: {message}")

    # This simulates invoking a Lambda function or similar service
    response = sns.publish(
        TopicArn=topic_arn,
        Message='A file was added to the queue'
    )
    print(f"Published message ID: {response['MessageId']}")

if __name__ == '__main__':
    sns_notifications()
