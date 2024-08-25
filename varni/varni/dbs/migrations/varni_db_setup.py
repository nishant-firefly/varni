import os
from shutil import copyfile
from dotenv import load_dotenv

REQUIRED_ENV_VARS = ['POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB', 'PROJECT_NAME']

def check_and_prompt_env_vars():
    missing_vars = []
    for var in REQUIRED_ENV_VARS:
        if not os.getenv(var):
            value = input(f"Enter value for {var}: ")
            os.environ[var] = value
            missing_vars.append(f"{var}={value}")
    
    if missing_vars:
        with open('.env', 'a') as env_file:
            env_file.write("\n".join(missing_vars) + "\n")

def setup_project_files():
    check_and_prompt_env_vars()

    project_dir = os.getenv('PROJECT_NAME')
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    dbs_dir = os.path.join(os.path.dirname(__file__), '..')

    files_to_create = [
        ('alembic.ini', os.path.join(template_dir, 'alembic.ini.template')),
        ('env.py', os.path.join(template_dir, 'env.py.template')),
    ]

    for filename, template_path in files_to_create:
        dest_path = os.path.join(project_dir, filename)
        if not os.path.exists(dest_path):
            if filename == 'alembic.ini':
                create_alembic_ini(dest_path, template_path)
            else:
                copyfile(template_path, dest_path)
                print(f"Created {filename} from template.")
        else:
            print(f"{filename} already exists, skipping.")

    create_docker_compose_yaml()

def create_alembic_ini(dest_path, template_path):
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    # Dynamically construct DATABASE_URL
    database_url = f"postgresql://{os.getenv('POSTGRES
