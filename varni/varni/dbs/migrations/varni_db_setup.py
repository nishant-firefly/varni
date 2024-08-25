import os
from shutil import copyfile
from dotenv import load_dotenv

# Define required environment variables
REQUIRED_ENV_VARS = ['POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB', 'PROJECT_NAME']

def check_and_prompt_env_vars():
    """Check for missing environment variables and prompt the user to input them."""
    missing_vars = []
    for var in REQUIRED_ENV_VARS:
        if not os.getenv(var):
            value = input(f"Enter value for {var}: ")
            os.environ[var] = value
            missing_vars.append(f"{var}={value}")
    
    if missing_vars:
        # Append missing variables to the .env file
        with open('.env', 'a') as env_file:
            env_file.write("\n".join(missing_vars) + "\n")

def setup_project_files():
    """Set up project configuration files and Docker Compose YAML."""
    check_and_prompt_env_vars()

    project_dir = os.getenv('PROJECT_NAME')
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    dbs_dir = os.path.join(os.path.dirname(__file__), '..')

    # Ensure the project directory exists
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)

    files_to_create = [
        ('alembic.ini', os.path.join(template_dir, 'alembic.ini.template')),
        ('env.py', os.path.join(template_dir, 'env.py.template')),
    ]

    for filename, template_path in files_to_create:
        dest_path = os.path.join(project_dir, filename)
        if not os.path.exists(dest_path):
            if os.path.exists(template_path):
                if filename == 'alembic.ini':
                    create_alembic_ini(dest_path, template_path)
                else:
                    copyfile(template_path, dest_path)
                    print(f"Created {filename} from template.")
            else:
                print(f"Template {template_path} not found, skipping {filename}.")
        else:
            print(f"{filename} already exists, skipping.")

    create_docker_compose_yaml()

def create_alembic_ini(dest_path, template_path):
    """Create the alembic.ini file with dynamically generated DATABASE_URL."""
    # Ensure the destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    # Dynamically construct DATABASE_URL
    database_url = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost/{os.getenv('POSTGRES_DB')}"

    # Replace placeholder with DATABASE_URL
    filled_content = template_content.replace('${DATABASE_URL}', database_url)

    with open(dest_path, 'w') as dest_file:
        dest_file.write(filled_content)
        print("Created alembic.ini with dynamically generated DATABASE_URL.")

def create_docker_compose_yaml():
    """Prompt the user to include Elasticsearch in the Docker Compose setup."""
    include_es = input("Do you want to include Elasticsearch in the Docker Compose setup? (y/n): ").strip().lower()
    if include_es == 'y':
        project_dir = os.getenv('PROJECT_NAME')
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'elastic_postgres_docker-compose.yaml.template')
        dest_path = os.path.join(project_dir, 'elastic_postgres_docker-compose.yaml')

        if not os.path.exists(dest_path):
            if os.path.exists(template_path):
                with open(template_path, 'r') as template_file:
                    template_content = template_file.read()

                # Replace placeholders with values from .env
                filled_content = template_content.format(
                    POSTGRES_USER=os.getenv('POSTGRES_USER'),
                    POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD'),
                    POSTGRES_DB=os.getenv('POSTGRES_DB')
                )

                # Ensure the destination directory exists
                dest_dir = os.path.dirname(dest_path)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                with open(dest_path, 'w') as dest_file:
                    dest_file.write(filled_content)
                    print("Created elastic_postgres_docker-compose.yaml with environment variables.")
            else:
                print(f"Template {template_path} not found, skipping Docker Compose setup.")
        else:
            print("elastic_postgres_docker-compose.yaml already exists, skipping.")

def main():
    """Main function to trigger the setup process."""
    setup_project_files()

if __name__ == "__main__":
    main()
