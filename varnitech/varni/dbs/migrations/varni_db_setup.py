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
        # 'alembic.ini': os.path.join(template_dir, 'alembic.ini.template'),
        # 'env.py': os.path.join(template_dir, 'env.py.template'),
        # 'manage.py': os.path.join(template_dir, 'manage.py.template'),
        # Files that go into the models directory
        'auth_models.py': os.path.join(os.path.dirname(__file__), '../auth/models.py'),
        # 'example_model.py': os.path.join(template_dir, 'example_model.py.template'),
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
        template_path = os.path.join(os.path.dirname(__file__), 'templates',
                                     'elastic_postgres_docker-compose.yaml.template')
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


# def main():
#     """Main function to trigger the setup process."""
#     setup_project_files()


import os
import subprocess
from urllib.parse import quote
import getpass  # For securely prompting for the password


def update_alembic_ini(alembic_ini_path, db_url):
    # Read the current alembic.ini file
    with open(alembic_ini_path, 'r') as file:
        lines = file.readlines()

    # Update the sqlalchemy.url line with the correct URL
    with open(alembic_ini_path, 'w') as file:
        for line in lines:
            if line.startswith('sqlalchemy.url'):
                file.write(f'sqlalchemy.url = {db_url}\n')
            else:
                file.write(line)


def create_env_py(env_py_path, db_url):
    env_py_content = f"""\
import logging
import os
import importlib
from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import registry

# Initialize an empty MetaData object using registry
mapper_registry = registry()
Base = mapper_registry.generate_base()
target_metadata = mapper_registry.metadata

# Define the path to the models directory (one level up from the alembic directory)
models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models'))

# Dynamically import all modules from the 'models' directory
for filename in os.listdir(models_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = 'models.' + filename[:-3]
        module = importlib.import_module(module_name)
        if hasattr(module, 'Base'):
            for table in module.Base.metadata.tables.values():
                if table not in target_metadata.tables:
                    target_metadata._add_table(table.name, table.schema, table)

config = context.config
config.set_main_option('sqlalchemy.url', '{db_url}')  # Replace with your actual PostgreSQL URL

logging.basicConfig()
logger = logging.getLogger('alembic.runtime.migration')
logger.setLevel(logging.INFO)

def run_migrations_online():
    engine = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    raise Exception("Offline mode is not supported")
else:
    run_migrations_online()
"""
    with open(env_py_path, 'w') as f:
        f.write(env_py_content)


def run_alembic_commands(db_url):
    project_dir = os.getenv('PROJECT_NAME')
    alembic_dir = os.path.join(project_dir, 'alembic')

    # Initialize Alembic if the directory doesn't exist
    if not os.path.exists(alembic_dir):
        subprocess.run(["alembic", "init", "alembic"], check=True, cwd=project_dir)

    # Path to files
    alembic_ini_path = os.path.join(project_dir, 'alembic.ini')
    env_py_path = os.path.join(alembic_dir, 'env.py')

    # Update alembic.ini with the correct SQLAlchemy URL
    update_alembic_ini(alembic_ini_path, db_url)

    # Create or update env.py
    create_env_py(env_py_path, db_url)

    # Check if alembic/versions is empty
    if not os.listdir(os.path.join(alembic_dir, 'versions')):
        # Generate migration script
        subprocess.run(["alembic", "revision", "--autogenerate", "-m", "Initial migration"], check=True,
                       cwd=project_dir)

    # Apply migration
    subprocess.run(["alembic", "upgrade", "head"], check=True, cwd=project_dir)


def main():
    """Main function to trigger the setup process."""
    setup_project_files()

    # Prompt user for PostgreSQL connection details
    username = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST', 'localhost')
    port = os.getenv('POSTGRES_PORT', '5432')
    database = os.getenv('POSTGRES_DB')

    # URL-encode the password
    encoded_password = quote(password)

    # Replace '%' with '%%' to escape it in the configuration file
    encoded_password = encoded_password.replace('%', '%%')

    # Construct the database URL
    db_url = f'postgresql://{username}:{encoded_password}@{host}:{port}/{database}'

    # Run Alembic commands with the constructed database URL
    run_alembic_commands(db_url)


if __name__ == "__main__":
    main()

