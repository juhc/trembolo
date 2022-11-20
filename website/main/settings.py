import os

SECRET_KEY = os.urandom(32).hex()
DB_NAME = f"{os.getcwd()}\\website\\trembolo.db"