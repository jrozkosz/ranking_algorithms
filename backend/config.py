from dotenv import load_dotenv
import os
import redis

load_dotenv()

class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SECURITY_PASSWORD_SALT = 'my_precious_two'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{os.environ["MYSQL_USER"]}:{os.environ["MYSQL_PASSWORD"]}@localhost:{os.environ["MYSQL_PORT"]}/{os.environ["MYSQL_DB_NAME"]}'

    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True # jezeli nie wykorzystuje secret_key to to dać na false
    SESSION_REDIS = redis.from_url(f'redis://127.0.0.1:{os.environ["REDIS_PORT"]}')
    
    # mail settings
    MAIL_DEFAULT_SENDER = "ranking.app.auth@gmail.com"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = f'{os.environ["EMAIL_PORT"]}'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = os.environ["EMAIL_USERNAME"]
    MAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
    # MAIL_DEFAULT_SENDER = "flaskapp@fastmail.com"
    # MAIL_SERVER = "smtp.fastmail.com"
    # MAIL_PORT = 465
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    # MAIL_DEBUG = False
    # MAIL_USERNAME = os.environ["EMAIL_USERNAME"]
    # MAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

    # CORS_HEADERS = 'Content-Type'
    
class TestConfig(ApplicationConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
