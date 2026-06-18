import os

from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this_value_should_be_updated'
    DEBUG = True

    DATABASE_URL = os.environ.get('DATABASE_URL', None)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///' + os.path.join(base_dir, 'oauth.sqlite')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OAUTH_CACHE_DIR = '_cache'

    MAIL_SERVER = None
    LOG_TO_STDOUT = None

    STORAGE_BACKEND = os.environ.get('STORAGE_BACKEND', 'csv')
    CSV_REQUIREMENT_PATH = os.environ.get(
        'CSV_REQUIREMENT_PATH',
        os.path.join(os.path.abspath(''), 'examples', 'specifications.csv'))
    OXYGRAPH_URL = os.environ.get('OXYGRAPH_URL', 'http://127.0.0.1:7878')
