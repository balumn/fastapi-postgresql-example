# FastAPI User Registration with PostgreSQL and MongoDB

This project is a user registration system implemented using FastAPI, PostgreSQL, and MongoDB. The application allows users to register by providing their Full Name, Email, Password, Phone, and Profile Picture. The user information is stored in PostgreSQL for fields like First Name, Password, Email, and Phone, while the Profile Picture is stored in MongoDB.

## Setup and Installation

Follow these steps to set up the project on your local machine:

1. Basic Setup:
    ```
    git clone git@github.com:balumn/fastapi-postgresql-example.git
    cd fastapi-user-registration
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
    cp sample.env .env
    ```

2. Configure the PostgreSQL and MongoDB databases:

   - Create a PostgreSQL database and update the connection details in `.env` file
   - Create a MongoDB database and update the connection details in `.env` file
   - if you are lazy enough:
     - MongoDB: https://gist.github.com/balumn/ee1af87e1a64201784fdfe55ae9aad98
     - PSQL: https://gist.github.com/balumn/fa3b536952c178e95d9e8de0b3487752

3. Run the FastAPI application:
   ```commandline
   uvicorn main:app --reload --port 8000
   ```

    The application will be accessible at http://127.0.0.1:8000.

# API Endpoints

The API provides the following endpoints:
 - You can access the API documentations on
   - http://127.0.0.1:8000/docs
   - http://127.0.0.1:8000/redoc


## Project Structure

The project is organized into the following directories and files:

```commandline
|-- Readme.md
|-- alembic.ini
|-- app <project root dir>
|   |-- __init__.py
|   |-- config.py <handles environment variables>
|   |-- core
|   |   |-- database
|   |   |   |-- __init__.py
|   |   |   |-- db.py <psql-sqlalchemy connection configs>
|   |   |   `-- db_util.py <fetching psql connection from pool>
|   |   |-- schemas.py <pydantic models>
|   |   `-- sql_models.py <sqlalchemy models>
|   |-- main.py
|   `-- v1
|       |-- api.py <holds all routes for v1>
|       |-- routes
|       |   `-- user.py <user routes>
|       |-- services
|       |   `-- user.py <user service file: CRUD logic, db queries for user>
|       |-- utils.py <common util functions>
|       `-- validators.py <pydantic validators>
|-- db <alembic settings>
|   |-- README
|   |-- env.py
|   |-- script.py.mako
|   `-- versions
|       `-- <holds alembic migrations>
|-- requirements.txt
`-- sample.env <sample env file; make sure you create a .env file>

```


# Dependencies

- FastAPI: Web framework for building APIs with Python.
- SQLAlchemy: ORM (Object-Relational Mapping) for working with PostgreSQL.
- pymongo: MongoDB driver for Python.
- alembic: Handling SQL migrations.
- Pydantic V2: Data validation and serialization library.
- uvicorn: ASGI server for running the FastAPI application.

# TODO
 - Dockerize FastAPI app
 - Create a docker-compose involving FastAPI, Postgre and MongoDB for development.