import os

SECRET_KEY = os.urandom(32).hex()
DB_NAME = f"{os.getcwd()}\\website\\trembolo.db"
MAIL_PORT = 465
MAIL_SERVER = 'smtp.mail.ru'
MAIL_USERNAME = 'trembolonotification@mail.ru'
MAIL_PASSWORD = 's1jrHcXDLRjVFsjrV09K'
MAIL_USE_TLS = False
MAIL_USE_SSL = True