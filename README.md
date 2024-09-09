
# AWS LocalStack Project

This project sets up a local development environment using LocalStack to simulate AWS services including SQS, SNS, IAM, Lambda, Step Functions, and S3. PostgreSQL is used for data storage, and FastAPI provides an API to interact with the data and AWS services.

## Project Structure

aws_local_project/ │ ├── api/ │ ├── init.py │ ├── endpoints.py │ ├── aws_resources/ │ ├── lambda_function.py │ ├── create_resources.py │ ├── step_function.json │ ├── db/ │ ├── init.sql │ ├── docker-compose.yml ├── Dockerfile ├── main.py ├── requirements.txt └── README.md



## Prerequisites

Ensure you have the following installed on your machine:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) (optional, for managing AWS resources)

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/aws_local_project.git
   cd aws_local_project


## Build and Start Docker Containers

docker-compose up --build

** This will start LocalStack, PostgreSQL, and FastAPI services. **

## Create AWS Resources
** Once the containers are up, create the necessary AWS resources (IAM roles, Lambda function, S3 bucket, Step Functions) using the provided Python script: **

docker exec -it api python aws_resources/create_resources.py
or 
python create_resources.py





## Usage
## FastAPI Application

The FastAPI application will be available at http://localhost:8000. You can use the following endpoints:

**Create Message: POST /messages/**
Example request body: {"content": "Hello World"}

**Get Messages: GET /messages/**
Retrieves all messages from PostgreSQL.

**Invoke Step Function: POST /invoke-step-function/**
Triggers the Step Function to invoke the Lambda function.

## AWS CLI (Optional)

If you want to interact with LocalStack services using AWS CLI, use the following commands:

**List SQS Queues:**
aws --endpoint-url=http://localhost:4566 sqs list-queues

**List SNS Topics:**
aws --endpoint-url=http://localhost:4566 sns list-topics


**List IAM Roles:**
aws --endpoint-url=http://localhost:4566 iam list-roles


**List Step Functions State Machines:**
aws --endpoint-url=http://localhost:4566 stepfunctions list-state-machines



### Summary

1. **Project Overview**: Provides a brief description and project structure.
2. **Prerequisites**: Lists software requirements.
3. **Setup**: Instructions to clone the repo, build containers, and create AWS resources.
4. **Usage**: Details how to interact with the FastAPI app and AWS services.
5. **Testing**: Example commands to test endpoints.
6. **Stopping**: Instructions to stop the Docker containers.
7. **Troubleshooting**: Common issues and solutions.
8. **License and Acknowledgments**: Licensing information and credits.

Replace `https://github.com/nishant-firefly/varni.git` with your actual repository URL if you’re sharing this on GitHub or another platform.
1. **Branch Name** : step_iam_s3_lambda_sqs_sns
(Add project files to aws_s3_step_iam_lambda_sqs_sns_services)
