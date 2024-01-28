"""[General Configuration Params]
"""
from os import environ, path
import os
from dotenv import load_dotenv
from datetime import timedelta

basedir = path.abspath(path.dirname(__file__))

load_dotenv(path.join(basedir, ".env"))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ["SQLALCHEMY_TRACK_MODIFICATIONS"]
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.environ["JWT_ACCESS_TOKEN_EXPIRES"])
    )
    URL = os.environ["URL"]


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
