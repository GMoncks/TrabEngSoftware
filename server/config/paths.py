import os

# Path do repositorio (fora da pasta atual)
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UTILS_FOLDER = os.path.join(BASE_PATH, 'utils')

DATABASE_FOLDER = os.path.join(UTILS_FOLDER, 'database')
DATABASE_PATH = os.path.join(DATABASE_FOLDER, 'sqlite_database.db')

SERVER_PORT = 8000
SERVER_BASE_URL = '/api'
