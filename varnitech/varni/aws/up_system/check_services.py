import subprocess
import os
from dotenv import load_dotenv
from docopt import docopt

def run_aws_command(service, endpoint_url, region_name):
    """Run an AWS CLI command based on the service and print the output."""
    # Define commands for each service
    commands = {
        's3': ['aws', 's3', 'ls'],
        'lambda': ['aws', 'lambda', 'list-functions'],
        'stepfunctions': ['aws', 'stepfunctions', 'list-state-machines'],
        'dynamodb': ['aws', 'dynamodb', 'list-tables'],
        'iam': ['aws', 'iam', 'list-roles']
    }
    
    if service not in commands:
        print(f"Service '{service}' is not supported.")
        return
    
    command = commands[service]
    
    # Add endpoint URL and region to the command
    command += ['--endpoint-url', endpoint_url, '--region', region_name]
    
    print(f"Checking {service}...")
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.stdout.strip():
            print(f"{service.capitalize()} service is running. Output:\n{result.stdout}")
        else:
            print(f"{service.capitalize()} service is running but no data found.")
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip()
        if 'Unable to locate credentials' in error_message:
            print(f"Credentials issue: {error_message}")
        elif 'An error occurred' in error_message:
            print(f"Error occurred: {error_message}")
        else:
            print(f"Unknown error occurred for {service}: {error_message}")

def main(services):
    # Load environment variables from .env file
    load_dotenv(dotenv_path='.env')  # Update with the path to your .env file
    
    # Read environment variables
    endpoint_url = os.getenv('LOCALSTACK_ENDPOINT', 'http://localhost:4566')
    region_name = os.getenv('REGION_NAME', 'us-east-1')
    
    service_list = [service.strip() for service in services.split(',')]
    for service in service_list:
        run_aws_command(service, endpoint_url, region_name)

if __name__ == "__main__":
    usage = """
    Usage:
      check_services.py <services>
    
    Options:
      -h --help     Show this help message and exit.
      <services>    Comma-separated list of services to check. Available services: s3, lambda, stepfunctions, dynamodb, iam.
    
    Examples:
    
      python check_services.py s3
        Checking s3...
        s3 service is running. Output:
        (list of S3 buckets or no data found if there are no buckets)
    
      python check_services.py lambda
        Checking lambda...
        lambda service is running. Output:
        (list of Lambda functions or no data found if there are no functions)
    
      python check_services.py stepfunctions
        Checking stepfunctions...
        stepfunctions service is running. Output:
        (list of Step Functions state machines or no data found if there are no state machines)
    
      python check_services.py dynamodb
        Checking dynamodb...
        dynamodb service is running. Output:
        (list of DynamoDB tables or no data found if there are no tables)
    
      python check_services.py s3,lambda,stepfunctions,dynamodb
        Checking s3...
        s3 service is running. Output:
        (list of S3 buckets or no data found if there are no buckets)
        Checking lambda...
        lambda service is running. Output:
        (list of Lambda functions or no data found if there are no functions)
        Checking stepfunctions...
        stepfunctions service is running. Output:
        (list of Step Functions state machines or no data found if there are no state machines)
        Checking dynamodb...
        dynamodb service is running. Output:
        (list of DynamoDB tables or no data found if there are no tables)
    """
    
    arguments = docopt(usage)
    services = arguments['<services>']
    main(services)
