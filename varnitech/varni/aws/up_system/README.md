# Set Up System

Welcome to the setup guide. This document provides instructions for setting up your local environment using LocalStack, Python and Docker. Please follow the steps outlined below to configure and start your services.

## Installation

### LocalStack with Docker

For a detailed installation guide for LocalStack, please refer to our [Installation Document](https://docs.google.com/document/d/1o_DJDGDltexrNTf4f1FwmJNnVJGHw6XuyiyKcsxeGN4/edit?usp=sharing).

## Configuration

### One-Time Setup: Generating Environment Variables

Before you begin using the system, you need to generate a `.env` file that will store your AWS credentials and other configuration settings from `config.json`. This is a one-time setup process, necessary for initializing your environment.

#### Install Dependencies 
```bash
# Assuming python3.11+ is installed 
cd path/to/aws # root folder 
## Can create virual environment and run 
pip install -r requirements.txt
pip install packages/varni
```
#### Generate AWS Credentials and Configuration

To create the `.env` file with AWS secrets, keys, and configurations, run the following command. This will setup the initial configuration and generate new AWS credentials:

```bash
# Navigate to the system setup directory
cd path/to/up_system

# Generate environment variables and AWS credentials
python generate_env.py --change-aws-creds
```

## Running the System
Once the configuration is in place, you can start LocalStack to simulate the AWS environment on your local machine:

### Start LocalStack services with Docker Compose 
```bash
# Navigate to the LocalStack directory
cd path/to/up_system
docker-compose up
```

### Routine Configuration Updates
If you need to update the values from config.json into the .env file after the initial setup, you can do so by running the following command:

```bash
# Navigate to the system setup directory
cd path/to/up_system

# Update configuration in the .env file
python generate_env.py
```

# Test the services status

## Install AWS CLI

1. **Visit the AWS CLI Installation Guide:**
   Go to the official AWS CLI installation guide for detailed instructions:
   [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

2. **Follow the Instructions:**
   Follow the installation instructions specific to your operating system as provided in the guide.
3. **Verify Installation:**

   To verify that AWS CLI has been installed correctly, open your terminal or command prompt and run:

   ```bash
   aws --version
   ```
4. **Check Services:**

   4.1 To get the help text:

   ```bash
   python check_services.py -h 
   ```
   
   Help Details with all examples.

   4.2 To check the status of AWS services, use the following command:

   ```bash
   python check_services.py <services>
   ```
   Replace <services> with a comma-separated list of the services you want to check. Available services are: s3, lambda, stepfunctions, dynamodb, iam.
   ```
   aws\up_system$ python3 check_services.py fakeservice,stepfunctions,s3,lambda,dynamodb
    Service 'fakeservice' is not supported.
    Checking stepfunctions...
    Stepfunctions service is running. Output:
    {# Test the Services Status

## Install AWS CLI

1. **Visit the AWS CLI Installation Guide:**
   Go to the official AWS CLI installation guide for detailed instructions:
   [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

2. **Follow the Instructions:**
   Follow the installation instructions specific to your operating system as provided in the guide.

3. **Verify Installation:**

   To verify that AWS CLI has been installed correctly, open your terminal or command prompt and run:

   ```bash
   aws --version
   ```
4. **Check Serrvices Examples:**

   4.1 Help Text:
   To display the help text and available commands, run:
   ```bash
   python check_services.py -h
   ```
   This will show you how to use the script and the available options.

   4.2 To check the status of AWS services, use the following command:
   ```bash
   python check_services.py <services>
   ```
   Replace <services> with a comma-separated list of the services you want to check. Available services are: s3, lambda, stepfunctions, dynamodb, iam.

   4.3 Examples:
   Check S3 Service:
   ```bash
   python check_services.py s3
   ```
   Output:
    ```yaml Checking s3...
    s3 service is running. Output: (list of S3 buckets or no data found if there are no buckets)
    ```
        "stateMachines": []
    }

    Checking s3...
    S3 service is running but no data found.
    Checking lambda...
    Lambda service is running. Output:
    {
        "Functions": []
    }

    Checking dynamodb...
    Error occurred: An error occurred (InternalFailure) when calling the ListTables operation: Service 'dynamodb' is not enabled. Please check your 'SERVICES' configuration variable.

   ```
