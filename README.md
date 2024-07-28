#IoT API

This project presents a simple web application for managing IoT devices. The application uses a PostgreSQL database to store information about devices, API users, and locations. The API is implemented using `aiohttp`, an asynchronous framework for Python.

## Overview.

- **Database**: PostgreSQL
- **ORM**: peewee
- Web framework: aiohttp
- Testing**: pytest

## Requirements.

1. Python 3.7 or later
2. PostgreSQL
3. Docker (to run in a container, optional)

## Settings

### Local configuration

1. Clone the repository:

    ###bash
    git clone https://github.com/yourusername/IoT_api.git
    cd IoT_api
    ```

2. Create and activate the virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate # Unix/MacOS
    .\.venv\Scripts\activate # Windows
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database. Create a PostgreSQL database and a user with appropriate rights. Update the `config.py` file with your data to connect to the database.

5. Initialize the database:

    ```bash
    python app.py
    ```

### Starting the application

To start the API:

```bash
python app.py
