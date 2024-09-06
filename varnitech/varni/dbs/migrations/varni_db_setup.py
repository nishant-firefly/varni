import os
from pathlib import Path
from shutil import copyfile
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define required environment variables
REQUIRED_ENV_VARS = ['POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB', 'PROJECT_NAME']

def check_and_prompt_env_vars():
    """Check for missing environment variables and prompt the user to input them."""
    missing_vars = {}
    for var in REQUIRED_ENV_VARS:
        value = os.getenv(var)
        if not value:
            user_input = input(f"Enter value for {var}: ")
            missing_vars[var] = user_input

    if missing_vars:
        # Append missing variables to the .env file
        with open('.env', 'a') as env_file:
            for key, value in missing_vars.items():
                env_file.write(f"{key}={value}\n")
                os.environ[key] = value  # Update environment variables in the current session

def setup_project_files():
    """Set up project configuration files, models directory, and Docker Compose YAML."""
    check_and_prompt_env_vars()

    project_dir = os.getenv('PROJECT_NAME')
    models_dir = os.path.join(project_dir, 'models')

    # Ensure the project and models directories exist
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
        print(f"Created project directory at {project_dir}")

    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        print(f"Created models directory at {models_dir}")

    template_dir = os.path.join(os.path.dirname(__file__), 'templates')

    files_to_create = {
        'alembic.ini': os.path.join(template_dir, 'alembic.ini.template'),
        'env.py': os.path.join(template_dir, 'env.py.template'),
        'manage.py': os.path.join(template_dir, 'manage.py.template'),
        # Files that go into the models directory
        'auth_models.py': os.path.join(os.path.dirname(__file__), '../auth/models.py'),
        'example_model.py': os.path.join(template_dir, 'example_model.py.template'),
        'README.txt': os.path.join(template_dir, 'README.txt.template'),
    }

    for filename, template_path in files_to_create.items():
        if filename in ['auth_models.py', 'example_model.py', 'README.txt']:
            dest_path = os.path.join(models_dir, filename)
        else:
            dest_path = os.path.join(project_dir, filename)
        
        if not os.path.exists(dest_path):
            try:
                copyfile(template_path, dest_path)
                print(f"Copied {filename} to {dest_path}.")
            except Exception as e:
                print(f"Failed to copy {filename} to {dest_path}: {e}")
        else:
            print(f"{filename} already exists at {dest_path}, skipping.")

    create_docker_compose_yaml()

def create_docker_compose_yaml():
    """Prompt the user to include Elasticsearch in the Docker Compose setup."""
    include_es = input("Do you want to include Elasticsearch in the Docker Compose setup? (y/n): ").strip().lower()
    if include_es == 'y':
        project_dir = os.getenv('PROJECT_NAME')
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'elastic_postgres_docker-compose.yaml.template')
        dest_path = os.path.join(project_dir, 'docker-compose.yaml')

        if not os.path.exists(dest_path):
            with open(template_path, 'r') as template_file:
                template_content = template_file.read()

            # Replace placeholders with values from .env or environment variables
            filled_content = template_content.replace('${POSTGRES_USER}', os.getenv('POSTGRES_USER', 'postgres'))
            filled_content = filled_content.replace('${POSTGRES_PASSWORD}', os.getenv('POSTGRES_PASSWORD', '123'))
            filled_content = filled_content.replace('${POSTGRES_DB}', os.getenv('POSTGRES_DB', 'varni'))

            with open(dest_path, 'w') as dest_file:
                dest_file.write(filled_content)
                print("Created docker-compose.yaml with PostgreSQL and Elasticsearch services.")
        else:
            print("docker-compose.yaml already exists, skipping.")
    else:
        print("Skipping Docker Compose setup.")

def main():
    """Main function to trigger the setup process."""
    setup_project_files()

if __name__ == "__main__":
    main()
