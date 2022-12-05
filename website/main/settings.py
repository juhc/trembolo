import os

SECRET_KEY = os.urandom(32).hex()
DB_NAME = f"{os.getcwd()}\\website\\trembolo.db"
MAIL_PORT = 465
MAIL_SERVER = 'smtp.mail.ru '
MAIL_USERNAME = 'trembolonotification@mail.ru'
MAIL_PASSWORD = 'Trembolo2022'