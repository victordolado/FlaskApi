import configparser
import logging
import os
import project

config_file = './conf/config.cfg'
config_parser = configparser.ConfigParser()
config_parser.read(config_file)
config_flask_key = 'FLASK'

flask_configuration = config_parser[config_flask_key]
ACTUAL_API = flask_configuration.get("ACTUAL_API", "0.1")
APPLICATION_ROOT = flask_configuration.get('APPLICATION_ROOT', '/')


class Config(object):

    # Load configuration parameters from configuration file

    SECRET_KEY = flask_configuration.get('SECRET_KEY', os.urandom(20))
    JWT_SECRET_KEY = flask_configuration.get('JWT_SECRET_KEY', os.urandom(20))
    JWT_BLACKLIST_ENABLED = flask_configuration.getboolean('JWT_BLACKLIST_ENABLED', True)
    JWT_BLACKLIST_TOKEN_CHECKS = [x.strip() for x in flask_configuration.get('JWT_BLACKLIST_TOKEN_CHECKS', '').split(',')]

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = flask_configuration.get('SQLALCHEMY_DATABASE_URI', None)
    SQLALCHEMY_TRACK_MODIFICATIONS = [x.strip() for x in flask_configuration.get('SQLALCHEMY_TRACK_MODIFICATIONS', '').split(',')]


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


# == LOGGING CONFIGURATION ==


def setup_logger():
    """ Set up the root logger. Using logger = logging.getLogger(__name__) the properties are inherited."""
    # Load configuration elements from the configuration file
    config_log_key = 'LOGGING'
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    log_configuration = config_parser[config_log_key]
    # Create the root logger
    p_file_name = log_configuration['LOGGING_FILE_NAME']
    logger = logging.getLogger(project.__name__)   # The logger name if from the name of the class
    logger.setLevel(logging.DEBUG)  # Set the messages that are passed on the parent application
    # create file handler which logs even debug messages
    os.makedirs('logs', exist_ok=True)  # create folder if it does not exist
    fh = logging.FileHandler('logs/{file_name}.log'.format(file_name=p_file_name))
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
