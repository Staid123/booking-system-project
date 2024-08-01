import os

from dotenv import load_dotenv


env_file_path = '.env'

load_dotenv(dotenv_path=env_file_path)

###################################################
SMTP_USER = os.getenv("SMTP_USER")  #
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  #
SMTP_HOST = os.getenv("SMTP_HOST")  #
SMTP_PORT = os.getenv("SMTP_PORT")  #
###################################################