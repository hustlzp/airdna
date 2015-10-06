# coding: utf-8
from .default import Config


class DevelopmentConfig(Config):
    # App config
    DEBUG = True

    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = "mysql://root:password@localhost/1jingdian"
    #CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    #CELERY_RESULT_BACKEND='redis://localhost:6379'
    CELERY_RESULT_BACKEND='amqp://guest:guest@localhost:5672//'

    MAIL_ACCOUNT = ''
    MAIL_PASSWORD = ''
    MAIL_SMTP = 'smtp.qq.com'
    MAIL_SMTP_PORT = 25
    MAIL_FROM = 'AirDNA'
