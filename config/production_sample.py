# coding: utf-8
from .default import Config


class ProductionConfig(Config):
    # App config
    SECRET_KEY = "\xb5\xb3}#\xb7A\xcac\x9d0\xb6\x0f\x80z\x97\x00\x1e\xc0\xb8+\xe9)\xf0}"
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 7
    SESSION_COOKIE_NAME = '1jingdian_session'

    # Site domain
    SITE_DOMAIN = "http://www.1jingdian.com"

    # Db config
    SQLALCHEMY_DATABASE_URI = "mysql://root:password@host/1jingdian"

    # Upload set config
    UPLOADS_DEFAULT_URL = "%s/uploads/" % SITE_DOMAIN

    # Sentry
    SENTRY_DSN = ''

    #CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    #CELERY_RESULT_BACKEND='redis://localhost:6379'
    CELERY_RESULT_BACKEND='amqp://guest:guest@localhost:5672//'

    MAIL_ACCOUNT = ''
    MAIL_PASSWORD = ''
    MAIL_SMTP = 'smtp.qq.com'
    MAIL_SMTP_PORT = 25
    MAIL_FROM = 'AirDNA'
