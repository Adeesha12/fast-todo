import os
from dotenv import load_dotenv

load_dotenv()

# log
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

# secrets
JWT_SECRET = os.environ.get('JWT_SECRET', None)
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', None)

# Database
DB_NAME = os.environ.get('DB_NAME', 'fastapi_db')
DB_USERNAME = os.environ.get('DB_USERNAME', None)
DB_PASSWORD = os.environ.get('DB_PASSWORD', None)
DB_HOST = os.environ.get('DB_HOST', 'localhost')