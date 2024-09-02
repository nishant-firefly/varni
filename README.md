# AWS Lambda Function with API Gateway

## Project Overview

This project demonstrates the creation and deployment of an AWS Lambda function and its integration with API Gateway. The setup includes both `GET` and `POST` methods that are accessible via API Gateway. The Lambda function is configured to return a simple message, "Hello from Lambda!" when invoked.

## Setup Instructions

### Prerequisites

- [LocalStack](https://github.com/localstack/localstack) installed and running.
- [AWS CLI](https://aws.amazon.com/cli/) configured to interact with LocalStack.
- PowerShell or any command-line interface for executing commands.

### Create the Lambda Function

1. **Prepare the Lambda Function Code**

   Create a file named `lambda_function.py` with the following content:

   ```python
   def lambda_handler(event, context):
       return {
           'statusCode': 200,
           'body': 'Hello from Lambda!'
       }


Testing
In Postman:

POST Request:

URL: http://localhost:4566/restapis/6okh0vozql/test/_user_request_/myresource
Method: POST
Expected Response: Hello from Lambda!


GET Request:

URL: http://localhost:4566/restapis/6okh0vozql/test/_user_request_/myresource
Method: GET
Expected Response: Hello from Lambda!

In Browser:

Open the following URL to test the GET method:
http://localhost:4566/restapis/6okh0vozql/test/_user_request_/myresource
You should see: Hello from Lambda!