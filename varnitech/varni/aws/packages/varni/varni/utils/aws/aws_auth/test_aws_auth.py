import os
import json
import pytest
from moto import mock_aws
import boto3
from aws_auth.aws_auth import AWSAuth, AuthType, EnvVar, STSParam, SecretsManagerKeys, STSCredentialsKeys, ParameterStoreKeys, AWSServiceName, SecretsManagerResponseKeys

@pytest.fixture
def setup_environment():
    os.environ[EnvVar.AWS_ACCESS_KEY_ID.value] = 'test_access_key_id'
    os.environ[EnvVar.AWS_SECRET_ACCESS_KEY.value] = 'test_secret_access_key'
    os.environ[EnvVar.AWS_SESSION_TOKEN.value] = 'test_session_token'
    os.environ[EnvVar.AWS_SECRET_ID.value] = 'test_secret_id'
    os.environ[EnvVar.AWS_ACCESS_KEY_ID_PARAM.value] = 'test_access_key_id_param'
    os.environ[EnvVar.AWS_SECRET_ACCESS_KEY_PARAM.value] = 'test_secret_access_key_param'
    os.environ[EnvVar.AWS_SESSION_TOKEN_PARAM.value] = 'test_session_token_param'
    os.environ[STSParam.AWS_ROLE_ARN.value] = 'arn:aws:iam::123456789012:role/test-role'
    os.environ[STSParam.AWS_ROLE_SESSION_NAME.value] = 'test-session'

@mock_aws
def test_load_from_sts_assume_role(setup_environment):
    with mock_aws().start():
        sts_client = boto3.client(AWSServiceName.STS.value, region_name="us-east-1")
        role_arn = os.environ[STSParam.AWS_ROLE_ARN.value]
        role_session_name = os.environ[STSParam.AWS_ROLE_SESSION_NAME.value]

        # Mock the assume_role call
        response = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=role_session_name
        )

        auth = AWSAuth(AuthType.STS_ASSUME_ROLE)
        auth.load_credentials()

        assert auth.aws_access_key_id == response['Credentials']['AccessKeyId']
        assert auth.aws_secret_access_key == response['Credentials']['SecretAccessKey']
        assert auth.aws_session_token == response['Credentials']['SessionToken']

@mock_aws
def test_load_from_secrets_manager(setup_environment):
    with mock_aws().start():
        secrets_client = boto3.client(AWSServiceName.SECRETS_MANAGER.value, region_name="us-east-1")
        secret_id = os.environ[EnvVar.AWS_SECRET_ID.value]
        secret_string = json.dumps({
            SecretsManagerKeys.ACCESS_KEY_ID.value: 'test_access_key_id',
            SecretsManagerKeys.SECRET_ACCESS_KEY.value: 'test_secret_access_key',
            SecretsManagerKeys.SESSION_TOKEN.value: 'test_session_token'
        })

        secrets_client.create_secret(Name=secret_id, SecretString=secret_string)

        auth = AWSAuth(AuthType.SECRETS_MANAGER)
        auth.load_credentials()

        assert auth.aws_access_key_id == 'test_access_key_id'
        assert auth.aws_secret_access_key == 'test_secret_access_key'
        assert auth.aws_session_token == 'test_session_token'

@mock_aws
def test_load_from_parameter_store(setup_environment):
    with mock_aws().start():
        ssm_client = boto3.client(AWSServiceName.SSM.value, region_name="us-east-1")
        access_key_param = os.environ[EnvVar.AWS_ACCESS_KEY_ID_PARAM.value]
        secret_key_param = os.environ[EnvVar.AWS_SECRET_ACCESS_KEY_PARAM.value]
        session_token_param = os.environ[EnvVar.AWS_SESSION_TOKEN_PARAM.value]

        ssm_client.put_parameter(Name=access_key_param, Value='test_access_key_id', Type='String', Overwrite=True)
        ssm_client.put_parameter(Name=secret_key_param, Value='test_secret_access_key', Type='String', Overwrite=True)
        ssm_client.put_parameter(Name=session_token_param, Value='test_session_token', Type='String', Overwrite=True)

        auth = AWSAuth(AuthType.PARAMETER_STORE)
        auth.load_credentials()

        assert auth.aws_access_key_id == 'test_access_key_id'
        assert auth.aws_secret_access_key == 'test_secret_access_key'
        assert auth.aws_session_token == 'test_session_token'
