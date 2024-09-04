import boto3

def receive_message():
    session = boto3.Session()
    sqs = session.client('sqs', endpoint_url='http://localhost:4566')

    queue_url = 'http://localhost:4566/000000000000/fileQueue'  # Replace with your queue URL

    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1
    )
    messages = response.get('Messages', [])
    for message in messages:
        print(f"Message Body: {message['Body']}")
        receipt_handle = message['ReceiptHandle']
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print("Message deleted from queue")

if __name__ == '__main__':
    receive_message()
