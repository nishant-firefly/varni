# AWS Lambda with LocalStack

## Overview

This project demonstrates how to set up and invoke an AWS Lambda function using LocalStack, a local AWS cloud stack emulator. The setup includes creating a Lambda function, packaging it, and invoking it locally. 

## Project Structure

my_aws_lambda_poc/ │ ├── venv/ # Python virtual environment directory │ ├── lambda_poc.py # Python script to call the Lambda function │ ├── requirements.txt # File to list Python dependencies │ ├── README.md # Project documentation │ ├── .gitignore # Git ignore file to exclude files from version control │ └── lambda_function.py # Python file with Lambda function code


## Steps to Set Up and Test AWS Lambda with LocalStack

### 1. **Install and Run LocalStack**

   - **Pull the LocalStack Docker Image:**
     ```bash
     docker pull localstack/localstack
     ```

   - **Run LocalStack in a Docker Container:**
     ```bash
     docker run --rm -it -p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack
     ```

   - **Verify LocalStack is Running:**
     ```bash
     curl http://localhost:4566/_localstack/health
     ```

### 2. **Prepare Lambda Function Code**

   - **Create `lambda_function.py` File:**
     This file contains the code for your Lambda function. For example:
     ```python
     def lambda_handler(event, context):
         return {
             'statusCode': 200,
             'body': 'Hello from Lambda!'
         }
     ```

   - **Package the Lambda Function:**
     ```bash
     zip function.zip lambda_function.py
     ```

### 3. **Create and Deploy Lambda Function**

   - **Create Lambda Function Using AWS CLI:**
     ```bash
     aws --endpoint-url=http://localhost:4566 lambda create-function \
         --function-name my_lambda_function \
         --runtime python3.8 \
         --role arn:aws:iam::000000000000:role/execution_role \
         --handler lambda_function.lambda_handler \
         --zip-file fileb://function.zip
     ```

### 4. **Invoke Lambda Function**

   - **Invoke the Lambda Function and Check Output:**
     ```bash
     aws --endpoint-url=http://localhost:4566 lambda invoke \
         --function-name my_lambda_function \
         output.txt
     ```

   - **Check the Output:**
     ```bash
     cat output.txt
     ```

### 5. **View Logs**

   - **Retrieve CloudWatch Logs for Lambda Function:**
     ```bash
     aws --endpoint-url=http://localhost:4566 logs filter-log-events \
         --log-group-name /aws/lambda/my_lambda_function
     ```

## Additional Information

- **LocalStack Version:** 3.7.2.dev2
- **Lambda Runtime:** Python 3.8
- **Logs Location:** `/aws/lambda/my_lambda_function`

## Troubleshooting

- **Error

## Troubleshooting

- **Error: `ResourceConflictException` when invoking the Lambda function**
  - **Possible Cause:** The function may still be in the `Pending` state.
  - **Solution:** Wait a few moments and try invoking the function again.

- **Error: `zip: command not found`**
  - **Possible Cause:** The `zip` utility might not be installed in the Docker container.
  - **Solution:** Install the `zip` utility in the container or use Docker on your host machine to package the Lambda function.

- **Error: `docker: command not found`**
  - **Possible Cause:** The `docker` command might not be available in the environment where you are running commands.
  - **Solution:** Ensure Docker is installed and properly configured on your system.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, please contact:

- **Name:** Deepti Shukla
- **Email:** deeptishukla515@gmail.com

