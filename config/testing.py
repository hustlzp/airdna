# coding: utf-8
from .default import Config


class TestingConfig(Config):
    # App config
    TESTING = True

    # Disable csrf while testing
    WTF_CSRF_ENABLED = False

    # Db config
    SQLALCHEMY_DATABASE_URI = "sqlite:///%s/db/testing.sqlite3" % Config.PROJECT_PATH
    #CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    #CELERY_RESULT_BACKEND='redis://localhost:6379'
    CELERY_RESULT_BACKEND='amqp://guest:guest@localhost:5672//'

