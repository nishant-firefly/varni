import os
from dotenv import load_dotenv, set_key

def generate_env_file():
    """Generate or update the .env file with necessary configurations."""
    load_dotenv()

    env_vars = {
        'LOCALSTACK_ENDPOINT': 'http://localhost:4566',
        'REGION_NAME': 'us-east-1',
        'AWS_ACCESS_KEY_ID': 'test',
        'AWS_SECRET_ACCESS_KEY': 'test',
    }

    for key, value in env_vars.items():
        set_key('.env', key, value)

if __name__ == "__main__":
    generate_env_file()
