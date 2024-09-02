# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

# snippet-start:[python.example_code.sfn.Hello]
import boto3
import os
from dotenv import load_dotenv

def hello_stepfunctions(stepfunctions_client):
    """
    Use the AWS SDK for Python (Boto3) to create an AWS Step Functions client and list
    the state machines in your account. This list might be empty if you haven't created
    any state machines.
    This example uses the default settings specified in your shared credentials
    and config files.

    :param stepfunctions_client: A Boto3 Step Functions Client object.
    """
    print("Hello, Step Functions! Let's list up to 10 of your state machines:")
    state_machines = stepfunctions_client.list_state_machines(maxResults=10)
    for sm in state_machines["stateMachines"]:
        print(f"\t{sm['name']}: {sm['stateMachineArn']}")


if __name__ == "__main__":

    dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'up_system', '.env')
    load_dotenv(dotenv_path)
    print(dotenv_path, os.path.exists(dotenv_path))

    hello_stepfunctions(boto3.client("stepfunctions",
        region_name=os.getenv("REGION_NAME"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        endpoint_url=os.getenv("LOCALSTACK_ENDPOINT")  # If using LocalStack
    ))