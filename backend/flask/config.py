import os

def load_config():

    config = {
        "host": os.environ.get("DATABASE_IP"),
        "database": os.environ.get("DATABASE_NAME"),
        "user": os.environ.get("DATABASE_USERNAME"),
        "password": os.environ.get("DATABASE_PASSWORD")
    }

    return config