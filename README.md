HEAD
## Install : 
```cd <path to\varni\varnitech>```
    
```pip install -e .  # -e so live changes updated  will be reflected```

``` python -c "import varni; varni.how_to_setup()"```

``` Next : python varni-db-setup should set up the db elastic search with instructions ```

    

# My FastAPI JSON App

## Overview

This project is a FastAPI application that interacts with a PostgreSQL database. It includes endpoints to manage users, products, and orders. The application also has a setup to import data and initialize the database schema.

## File Structure

- `my_fastapi_json_app/`
  - `api/`
    - `crud.py`: Contains CRUD operations for database interactions.
    - `database.py`: Database connection and session management.
    - `endpoints.py`: FastAPI routes and endpoint definitions.
    - `models.py`: SQLAlchemy models defining the database schema.
    - `schemas.py`: Pydantic schemas for request and response validation.
  - `data/`
    - `orders.json`: Sample data for orders.
    - `products.json`: Sample data for products.
    - `users.json`: Sample data for users.
  - `tests/`
    - `test_endpoints.py`: Test cases for the FastAPI endpoints.
  - `utils/`: Utility functions and scripts.
  - `check_sqlalchemy_version.py`: Script to check SQLAlchemy version.
  - `config.py`: Configuration settings for the application.
  - `docker-compose.yml`: Docker Compose configuration file.
  - `import_data.py`: Script to import data from JSON files into the database.
  - `init_db.py`: Script to initialize the database schema.
  - `main.py`: Entry point for the FastAPI application.
  - `requirements.txt`: Python package dependencies.

## Setup and Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/nishant-firefly/varni.git

   cd varni/my_fastapi_json_app


2. **Create and Activate a Virtual Environment:**
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Dependencies:**

pip install -r requirements.txt

4.**Set Up the Database:**
## Run Docker Compose to Start PostgreSQL:

docker-compose up -d

## Import Sample Data:

python my_fastapi_json_app/import_data.py


5. **Database Operations**

## Database Setup
The Docker Compose file sets up PostgreSQL with the following configuration:

User: myuser
Password: mypassword
Database: mydatabase

## Connect to PostgreSQL

docker exec -it postgres-latest psql -U myuser -d mydatabase

or

psql -U myuser -h localhost -d mydatabase

## Verify the Data

\dt
SELECT * FROM users;
SELECT * FROM products;
SELECT * FROM orders;
\q

### Steps for README.md Creation

1. **Project Overview**: Summarize the purpose and components of your project.
2. **File Structure**: List and describe each file and directory in your project.
3. **Setup and Installation**:
   - Clone the repository.
   - Set up a virtual environment.
   - Install dependencies.
   - Configure and start the database.
4. **Database Operations**: Provide commands for interacting with the database.
5. **Docker Commands**: If Docker is used, include commands for building and managing Docker containers.
6. **Notes**: Any additional notes or configuration details.
7. **License**: Include a license section if applicable.

## Troubleshooting and Error

1. **Access the FastAPI application** at `http://localhost:8000`.
2. **Test API endpoints** to view the data.
3. **Running Tests**  pytest my_fastapi_json_app/tests/
4. **Initialize the Database Schema:** python my_fastapi_json_app/init_db.py
5. **Run the Application:** uvicorn my_fastapi_json_app.main:app --reload


Adjust the placeholders and commands based on your specific setup and environment.
(Initial commit with FastAPI and SQLAlchemy setup)
