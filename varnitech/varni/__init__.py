# File: varni/__init__.py

def how_to_setup():
    instructions = """
    How to Set Up Your Project with Varni:

    1. Create a .env file in your example_project directory with the following content:
       POSTGRES_USER=your_postgres_user
       POSTGRES_PASSWORD=your_postgres_password
       POSTGRES_DB=your_database_name
       MODEL_MODULES=varni.dbs.auth.models,example_project.models.custom_user
       PROJECT_NAME=example_project

    2. Run the following command from the example_project directory to set up your project:
       python -m varni-db-setup

       - This command will prompt you to enter any missing .env variables.
       - It will generate the necessary configuration files, including alembic.ini, env.py, and elastic_postgres_docker-compose.yaml (if desired).

    3. To manage database migrations, use the following commands:

       - Initialize the database:
         varni-migrate init

       - Create a new migration:
         varni-migrate migrate

       - Apply the latest migrations:
         varni-migrate update

       - Run all migrations:
         varni-migrate apply

    4. After running these commands, your project should be fully set up and ready for development!

    For more information or troubleshooting, please consult the documentation or reach out to the support team.
    """
    print(instructions)
