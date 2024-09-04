# from fastapi import APIRouter
# from scripts import send_message, receive_message, view_services

# router = APIRouter()

# @router.get("/sqs-queues")
# def list_queues():
#     return view_services.list_sqs_queues()

# @router.get("/sns-topics")
# def list_topics():
#     return view_services.list_sns_topics()

# @router.post("/send-message")
# def send_message_to_queue(message: str):
#     return send_message.send_message_to_queue(message)

# @router.get("/receive-message")
# def receive_message_from_queue():
#     return receive_message.receive_message_from_queue()


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3

app = FastAPI()

# Create SQS and SNS clients
sqs = boto3.client('sqs', endpoint_url='http://localhost.localstack.cloud:4566')
sns = boto3.client('sns', endpoint_url='http://localhost.localstack.cloud:4566')

class MessageModel(BaseModel):
    message_body: str
    message_attributes: dict = None

@app.get("/sqs/queues")
def list_sqs_queues():
    try:
        response = sqs.list_queues()
        return response.get('QueueUrls', [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sqs/send/{queue_url}")
def send_message_to_sqs(queue_url: str, message: MessageModel):
    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message.message_body,
            MessageAttributes=message.message_attributes or {}
        )
        return {"MessageId": response['MessageId']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sqs/receive/{queue_url}")
def receive_message_from_sqs(queue_url: str):
    try:
        response = sqs.receive_message(QueueUrl=queue_url)
        messages = response.get('Messages', [])
        if not messages:
            return {"message": "No messages available"}
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sns/topics")
def list_sns_topics():
    try:
        response = sns.list_topics()
        return response.get('Topics', [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sns/publish/{topic_arn}")
def publish_to_sns(topic_arn: str, message: MessageModel):
    try:
        response = sns.publish(
            TopicArn=topic_arn,
            Message=message.message_body,
            MessageAttributes=message.message_attributes or {}
        )
        return {"MessageId": response['MessageId']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
