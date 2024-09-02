# Introduction

_Nishant will fill this section._

---

## Installation

### Prerequisite

- **Install Docker**: _(Instructions will be filled by the Dev)_
- **Install Python**: _(Instructions will be filled by the Dev)_
  - Python version 3.11 or higher is required.
- **Activate Virtual Environment**: _(Instructions will be filled by the Dev)_

### Python Mode

#### Set Up Project (One Time)

1. **Navigate to the Project Directory**:
    ```bash
    cd varnitech
    ```

2. **Install Dependencies**:  
   To install all required dependencies listed in `requirements.txt`, run the following command:
    ```bash
    pip install -e .
    ```

3. **Set Up Docker Compose and Initial Migrations**:  
   Run the following command to set up the Docker Compose file and perform the initial database migrations:
    ```bash
    python -m varni initialize
    ```
   _Note: If you encounter any issues with the above command, use this alternative command instead:_
    ```bash
    python ..\varnitech\varni\dbs\migrations\varni_db_setup.py initialize
    ```

4. **Start Docker Containers**:  
   To start the Docker containers for Elasticsearch and PostgreSQL, use the following command:
    ```bash
    docker-compose -f elastic-postgres.yaml up -d
    ```

### Docker Mode

_Nishant will add structure/template and TODOS._  
_Lakshmi will fill the template with commands in Dockerfile and Docker Compose._

### Commands

- **Navigate to the New Project Directory**:  
  Before generating Alembic migration scripts, ensure you're in the correct project directory:
    ```bash
    cd new_project_directory_folder
    ```

- **Generate Alembic Migration Script**:  
  Run the following command to generate a new migration script based on changes in the models folder:
    ```bash
    alembic revision --autogenerate -m "Initial migration"
    ```
  _[alembic] This will run migrations based on changes detected in the models folder._
  
- **Apply Alembic Migrations**:  
  To apply the generated migration and update your database schema, use:
    ```bash
    alembic upgrade head
    ```
    
