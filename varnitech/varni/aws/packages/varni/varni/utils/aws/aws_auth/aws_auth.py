import boto3
import os
import json
from typing import Optional
from enum import Enum
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

class AuthType(Enum):
    ENVIRONMENT = 'environment'
    SHARED_CREDENTIALS = 'shared_credentials'
    STS_ASSUME_ROLE = 'sts_assume_role'
    SECRETS_MANAGER = 'secrets_manager'
    PARAMETER_STORE = 'parameter_store'

class EnvVar(Enum):
    AWS_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID'
    AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'
    AWS_SESSION_TOKEN = 'AWS_SESSION_TOKEN'
    AWS_SECRET_ID = 'AWS_SECRET_ID'
    AWS_ACCESS_KEY_ID_PARAM = 'AWS_ACCESS_KEY_ID_PARAM'
    AWS_SECRET_ACCESS_KEY_PARAM = 'AWS_SECRET_ACCESS_KEY_PARAM'
    AWS_SESSION_TOKEN_PARAM = 'AWS_SESSION_TOKEN_PARAM'

class STSParam(Enum):
    AWS_ROLE_ARN = 'AWS_ROLE_ARN'
    AWS_ROLE_SESSION_NAME = 'AWS_ROLE_SESSION_NAME'
    DEFAULT_ROLE_SESSION_NAME = 'AssumeRoleSession'

class STSCredentialsKeys(Enum):
    CREDENTIALS = 'Credentials'
    ACCESS_KEY_ID = 'AccessKeyId'
    SECRET_ACCESS_KEY = 'SecretAccessKey'
    SESSION_TOKEN = 'SessionToken'

class SecretsManagerKeys(Enum):
    ACCESS_KEY_ID = 'aws_access_key_id'
    SECRET_ACCESS_KEY = 'aws_secret_access_key'
    SESSION_TOKEN = 'aws_session_token'

class ParameterStoreKeys(Enum):
    VALUE = 'Value'

class AWSServiceName(Enum):
    SECRETS_MANAGER = 'secretsmanager'
    STS = 'sts'
    SSM = 'ssm'

class SecretsManagerResponseKeys(Enum):
    SECRET_STRING = 'SecretString'

class AWSAuth:
    def __init__(self, auth_type: AuthType):
        self.aws_access_key_id: Optional[str] = None
        self.aws_secret_access_key: Optional[str] = None
        self.aws_session_token: Optional[str] = None
        self.auth_type: AuthType = auth_type

    def load_from_environment(self):
        self.aws_access_key_id = os.getenv(EnvVar.AWS_ACCESS_KEY_ID.value)
        self.aws_secret_access_key = os.getenv(EnvVar.AWS_SECRET_ACCESS_KEY.value)
        self.aws_session_token = os.getenv(EnvVar.AWS_SESSION_TOKEN.value)

    def load_from_shared_credentials(self):
        try:
            session = boto3.Session()
            credentials = session.get_credentials().get_frozen_credentials()
            self.aws_access_key_id = credentials.access_key
            self.aws_secret_access_key = credentials.secret_key
            self.aws_session_token = credentials.token
        except (NoCredentialsError, PartialCredentialsError):
            pass

    def load_from_sts_assume_role(self):
        role_arn = os.getenv(STSParam.AWS_ROLE_ARN.value)
        role_session_name = os.getenv(STSParam.AWS_ROLE_SESSION_NAME.value, STSParam.DEFAULT_ROLE_SESSION_NAME.value)
        if role_arn:
            try:
                sts_client = boto3.client(AWSServiceName.STS.value)
                assumed_role = sts_client.assume_role(
                    RoleArn=role_arn,
                    RoleSessionName=role_session_name
                )
                credentials = assumed_role[STSCredentialsKeys.CREDENTIALS.value]
                self.aws_access_key_id = credentials[STSCredentialsKeys.ACCESS_KEY_ID.value]
                self.aws_secret_access_key = credentials[STSCredentialsKeys.SECRET_ACCESS_KEY.value]
                self.aws_session_token = credentials[STSCredentialsKeys.SESSION_TOKEN.value]
            except (NoCredentialsError, PartialCredentialsError, KeyError, ClientError):
                pass

    def load_from_secrets_manager(self):
        secret_id = os.getenv(EnvVar.AWS_SECRET_ID.value)
        if secret_id:
            try:
                secrets_client = boto3.client(AWSServiceName.SECRETS_MANAGER.value)
                secret_value = secrets_client.get_secret_value(SecretId=secret_id)
                secrets = json.loads(secret_value[SecretsManagerResponseKeys.SECRET_STRING.value])
                self.aws_access_key_id = secrets[SecretsManagerKeys.ACCESS_KEY_ID.value]
                self.aws_secret_access_key = secrets[SecretsManagerKeys.SECRET_ACCESS_KEY.value]
                self.aws_session_token = secrets[SecretsManagerKeys.SESSION_TOKEN.value]
            except (NoCredentialsError, PartialCredentialsError, KeyError, ClientError):
                pass

    def load_from_parameter_store(self):
        access_key_param = os.getenv(EnvVar.AWS_ACCESS_KEY_ID_PARAM.value)
        secret_key_param = os.getenv(EnvVar.AWS_SECRET_ACCESS_KEY_PARAM.value)
        session_token_param = os.getenv(EnvVar.AWS_SESSION_TOKEN_PARAM.value)
        if access_key_param and secret_key_param:
            try:
                ssm_client = boto3.client(AWSServiceName.SSM.value)
                self.aws_access_key_id = ssm_client.get_parameter(Name=access_key_param, WithDecryption=True)[ParameterStoreKeys.VALUE.value]
                self.aws_secret_access_key = ssm_client.get_parameter(Name=secret_key_param, WithDecryption=True)[ParameterStoreKeys.VALUE.value]
                if session_token_param:
                    self.aws_session_token = ssm_client.get_parameter(Name=session_token_param, WithDecryption=True)[ParameterStoreKeys.VALUE.value]
            except (NoCredentialsError, PartialCredentialsError, KeyError, ClientError):
                pass

    def load_credentials(self):
        if self.auth_type == AuthType.ENVIRONMENT:
            self.load_from_environment()
        elif self.auth_type == AuthType.SHARED_CREDENTIALS:
            self.load_from_shared_credentials()
        elif self.auth_type == AuthType.STS_ASSUME_ROLE:
            self.load_from_sts_assume_role()
        elif self.auth_type == AuthType.SECRETS_MANAGER:
            self.load_from_secrets_manager()
        elif self.auth_type == AuthType.PARAMETER_STORE:
            self.load_from_parameter_store()

    def is_valid(self) -> bool:
        return self.aws_access_key_id is not None and self.aws_secret_access_key is not None

    def create_s3_client(self):
        if self.is_valid():
            return boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                aws_session_token=self.aws_session_token
            )
        else:
            return boto3.client('s3')

def main():
    # Define the method you want to use
    auth_type = AuthType.ENVIRONMENT

    aws_creds = AWSAuth(auth_type)
    aws_creds.load_credentials()

    # Create the S3 client using the credentials
    s3_client = aws_creds.create_s3_client()

    # Example usage of the S3 client
    try:
        response = s3_client.list_buckets()
        print("Buckets:", [bucket['Name'] for bucket in response['Buckets']])
    except NoCredentialsError:
        print("Error: No AWS credentials found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
