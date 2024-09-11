# AWS Lambda Function with API Gateway

## Project Overview

This project demonstrates the creation and deployment of an AWS Lambda function and its integration with API Gateway. The setup includes both `GET` and `POST` methods that are accessible via API Gateway. The Lambda function is configured to return a simple message, "Hello from Lambda!" when invoked.

## Open your terminal or command prompt and execute the following commands:

cd my_aws_lambda_poc


Create and activate a Python virtual environment:
python -m venv venv
.\venv\Scripts\activate


docker-compose down
docker-compose up -d  (optional)

aws --endpoint-url=http://localhost:4566 lambda list-functions

## Verify if there were any issues during the Lambda function deployment. Run:

docker-compose logs localstack

## one-liner command to create a Lambda function:

aws --endpoint-url=http://localhost:4566 lambda create-function --function-name my_lambda_function --runtime python3.9 --zip-file fileb://function.zip --handler lambda_function.lambda_handler --role arn:aws:iam::000000000000:role/lambda-role


## Wait a bit and then check the status of the function again using:


aws --endpoint-url=http://localhost:4566 lambda get-function --function-name my_lambda_function


## invoke the function again:

aws --endpoint-url=http://localhost:4566 lambda invoke --function-name my_lambda_function --payload '{}' output.json

##  After invoking it, check the contents of output.json to see the result

type output.json




**Output :**

(venv) PS D:\my_aws_lambda_poc> aws --endpoint-url=http://localhost:4566 lambda invoke --function-name my_lambda_function --payload '{}' output.json
{
    "StatusCode": 200,
    "ExecutedVersion": "$LATEST"
}

(venv) PS D:\my_aws_lambda_poc> type output.json

{"statusCode": 200, "body": "Hello from Lambda!"}






## Setup Instructions

### Prerequisites

- [LocalStack](https://github.com/localstack/localstack) installed and running.
- [AWS CLI](https://aws.amazon.com/cli/) configured to interact with LocalStack.
- PowerShell or any command-line interface for executing commands.




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
