from varni.utils.aws.env_clients import get_aws_service_clients, SERVICES
import os 
from dotenv import load_dotenv
# path\to\aws\e2e\..\up_system\.env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'up_system', '.env')
load_dotenv(dotenv_path)
print(dotenv_path)
AWS_SERVICE_CLIENTS= get_aws_service_clients()
client_dynamodb = AWS_SERVICE_CLIENTS[SERVICES.DYNAMODB.value]
client_stepfunctions = AWS_SERVICE_CLIENTS[SERVICES.STEPFUNCTIONS.value]
client_lambda = AWS_SERVICE_CLIENTS[SERVICES.LAMBDA.value]