# File: varni/dbs/migrations/setup_files.py
import os
from shutil import copyfile
from dotenv import load_dotenv

load_dotenv()

def setup_project_files():
    project_dir = os.getenv('PROJECT_NAME')
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')

    files_to_create = [
        ('alembic.ini', os.path.join(template_dir, 'alembic.ini.template')),
        ('env.py', os.path.join(template_dir, 'env.py.template')),
    ]

    for filename, template_path in files_to_create:
        dest_path = os.path.join(project_dir, filename)
        if not os.path.exists(dest_path):
            copyfile(template_path, dest_path)
            print(f"Created {filename} from template.")
        else:
            print(f"{filename} already exists, skipping.")

if __name__ == "__main__":
    setup_project_files()
