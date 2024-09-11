
from utils import CONFIG_FILE, ENV_FILE
from utils import EnvFileManager,CONFIG_FILE, ENV_FILE
import boto3
class AwsService:
    def __init__(self, service_name="") -> None:
        envs=EnvFileManager(CONFIG_FILE,ENV_FILE).read_env()
        self.boto_client=boto3.client(service_name, **{
            "aws_access_key_id":envs.get("AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": envs.get("AWS_ACCESS_KEY_ID"),
            "region_name": envs.get("REGION_NAME"),
            "endpoint_url": f"{envs.get("LOCALSTACK_ENDPOINT")}/{service_name}"
        })
    def create(self, *args, **kwargs):
        raise NotImplementedError("Create method not implemented")

    def read(self, *args, **kwargs):
        raise NotImplementedError("Read method not implemented")

    def update(self, *args, **kwargs):
        raise NotImplementedError("Update method not implemented")

    def delete(self, *args, **kwargs):
        raise NotImplementedError("Delete method not implemented")

    def list(self, *args, **kwargs):
        raise NotImplementedError("List method not implemented")
