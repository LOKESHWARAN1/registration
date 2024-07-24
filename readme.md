# Registration

## Requirements
To get started with the project, ensure you have the following software installed:
- python - 3.10.12
- pip (Python package installer)
- PostgreSQL
- MongoDB


## Installation

Follow these steps to set up the project:

1. Clone the repository and navigate to the project directory:
    ```shell
    git clone https://github.com/LOKESHWARAN1/registration.git
    cd registration
    ```
2. Install the required Python packages:
    ```shell
    pip install -r requirements.txt
    ```

## Database config

The database connection details for PostgreSQL and MongoDB are specified in the `.env` file located in the root directory of the project. Make sure to update the `.env` file with your database credentials and other necessary configurations.

```
/registration       # This is the root directory
│
├── .env                  # Environment variables file
```

## Profile Picture Storage
User profile pictures are stored in the `profile_pictures` directory:
```
/registration
│
├── profile_pictures       # User profile pictures store in this directory
```

## Screenshots
Project screenshots are attached in the `screen_shot` directory:
```
/registration
│
├── screen_shot            # Project screen shot files are attached here
```

## Running the Application
To start the application, use the following command:

```shell
uvicorn src.main:app --reload
```
The `--reload` flag is used for automatic reloading when code changes. This is useful during development.

## Accessing the Application

After starting the application, you can verify the deployment by navigating to the following URL in your preferred browser:

```bash
http://localhost:8000/docs
```
This URL provides access to the Swagger UI, which documents and allows you to interact with the API endpoints.

## Conclusion
Your project is now set up and running. If you encounter any issues, please check the installation steps and ensure all dependencies are properly installed. For further assistance, refer to the documentation or contact the project maintainers.