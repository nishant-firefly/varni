import random
import string
import sys
from utils import CONFIG_FILE, ENV_FILE, EnvFileManager, ENV_STRS

class ConfigToEnvConverter(EnvFileManager):
    def convert(self):
        """Converts the JSON configuration to a .env file."""
        config = self.read_json()
        if config is not None:
            self.write_env(config)

class AWSCredentialsGenerator(EnvFileManager):
    def generate_credentials(self):
        """Simulates generating AWS credentials."""
        access_key = ENV_STRS['AKIA'] + ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        secret_key = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=40))
        print(ENV_STRS['aws_key_generated'])
        return {
            ENV_STRS['AWS_ACCESS_KEY_ID']: access_key,
            ENV_STRS['AWS_SECRET_ACCESS_KEY']: secret_key
        }

if __name__ == "__main__":
    converter = ConfigToEnvConverter(CONFIG_FILE, ENV_FILE)
    if '--change-aws-creds' in sys.argv:
        creds = AWSCredentialsGenerator(CONFIG_FILE, ENV_FILE).generate_credentials()
        converter.write_env(creds)
    
    # Update Config 
    ConfigToEnvConverter(CONFIG_FILE, ENV_FILE).convert()
