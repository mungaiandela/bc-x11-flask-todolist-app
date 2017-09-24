import os
from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Config(object):
    BASE_DIR = dirname(__file__)
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PAGE_LIMIT = 10
    DEFAULT_PAGE = 1


class DevelopmentConfiguration(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': os.getenv("FB_ID"),
            'secret': os.getenv("FB_SECRET")
        },
        'twitter': {
            'id': os.getenv("TWITTER_ID"),
            'secret': os.getenv("TWITTER_SECRET")
        }
    }


class TestingConfiguration(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + Config.BASE_DIR \
                              + "/test/test_db.sqlite"
    PAGE_LIMIT = 2


app_configuration = {
    'production': Config,
    'development': DevelopmentConfiguration,
    'testing': TestingConfiguration
}
