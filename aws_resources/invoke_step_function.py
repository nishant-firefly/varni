# import boto3
# import json
# import time

# # Initialize LocalStack resources
# localstack_endpoint = "http://localhost:4566"

# session = boto3.Session(
#     aws_access_key_id='test',
#     aws_secret_access_key='test',
#     region_name='us-east-1'
# )

# stepfunctions = session.client('stepfunctions', endpoint_url=localstack_endpoint)

# def start_step_function_execution():
#     try:
#         state_machine_arn = "arn:aws:states:us-east-1:000000000000:stateMachine:MyStateMachine"
#         input_payload = json.dumps({"key": "value"})  # Adjust based on Lambda's input

#         response = stepfunctions.start_execution(
#             stateMachineArn=state_machine_arn,
#             input=input_payload
#         )
        
#         print("Step Function execution started.")
#         print("Execution ARN:", response.get('executionArn'))
#         return response.get('executionArn')
        
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None

# def get_execution_status(execution_arn):
#     try:
#         response = stepfunctions.describe_execution(
#             executionArn=execution_arn
#         )
#         print("Execution Status:", response.get('status'))
#         if response.get('status') == 'SUCCEEDED':
#             print("Execution Output:", response.get('output'))
#         else:
#             print("Execution is still running.")
        
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     execution_arn = start_step_function_execution()
    
#     if execution_arn:
#         print("Waiting for Step Function to complete...")
#         time.sleep(5)  # Wait a few seconds to let the step function execute
        
#         get_execution_status(execution_arn)




#this below code is working=2 no


# import boto3
# import json

# # Initialize LocalStack resources
# localstack_endpoint = "http://localhost:4566"

# # Initialize Boto3 session
# session = boto3.Session(
#     aws_access_key_id='test',
#     aws_secret_access_key='test',
#     region_name='us-east-1'
# )

# stepfunctions = session.client('stepfunctions', endpoint_url=localstack_endpoint)

# def start_step_function_execution():
#     try:
#         # Replace this with your state machine ARN
#         state_machine_arn = "arn:aws:states:us-east-1:000000000000:stateMachine:MyStateMachine"
        
#         # Define the input payload
#         input_payload = json.dumps({"key": "value"})  # Customize this based on Lambda function input requirements
        
#         # Start Step Function execution
#         response = stepfunctions.start_execution(
#             stateMachineArn=state_machine_arn,
#             input=input_payload
#         )
        
#         print("Step Function execution started.")
#         print("Execution ARN:", response.get('executionArn'))
#         print("Start Date:", response.get('startDate'))
        
#         return response.get('executionArn')
        
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None

# def get_execution_status(execution_arn):
#     try:
#         response = stepfunctions.describe_execution(
#             executionArn=execution_arn
#         )
#         print("Execution Status:", response.get('status'))
#         print("Execution Output:", response.get('output'))
        
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     execution_arn = start_step_function_execution()
#     if execution_arn:
#         get_execution_status(execution_arn)


import boto3
import json
import time

# Initialize LocalStack resources
localstack_endpoint = "http://localhost:4566"

# Initialize Boto3 session
session = boto3.Session(
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

stepfunctions = session.client('stepfunctions', endpoint_url=localstack_endpoint)

def start_step_function_execution():
    try:
        # Replace this with your state machine ARN
        state_machine_arn = "arn:aws:states:us-east-1:000000000000:stateMachine:MyStateMachine"
        
        # Define the input payload
        input_payload = json.dumps({"key": "value"})  # Customize this based on your needs
        
        # Start Step Function execution
        response = stepfunctions.start_execution(
            stateMachineArn=state_machine_arn,
            input=input_payload
        )
        
        print("Step Function execution started.")
        print("Execution ARN:", response.get('executionArn'))
        print("Start Date:", response.get('startDate'))
        
        return response.get('executionArn')
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_execution_status(execution_arn):
    try:
        response = stepfunctions.describe_execution(
            executionArn=execution_arn
        )
        print("Execution Status:", response.get('status'))
        print("Execution Output:", response.get('output'))
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    execution_arn = start_step_function_execution()
    if execution_arn:
        # Poll for status until the execution is complete
        while True:
            time.sleep(5)  # Wait for 5 seconds before checking status again
            response = stepfunctions.describe_execution(executionArn=execution_arn)
            status = response.get('status')
            print("Execution Status:", status)
            if status in ['SUCCEEDED', 'FAILED', 'TIMED_OUT', 'ABORTED']:
                print("Execution Output:", response.get('output'))
                break

