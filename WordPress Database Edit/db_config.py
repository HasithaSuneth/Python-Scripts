import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('HOST', 'localhost')
user = os.getenv('USER', 'db_user')
password = os.getenv('PASSWORD', 'password')
database = os.getenv('DATABASE', 'database')

db_config = {
    "host": host,
    "user": user,
    "password": password,
    "database": database
}

table_prefix = os.getenv('TABLE_PREFIX', 'wp_')