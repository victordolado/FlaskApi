"""
The init file at this level loads all the needed configuration to modify the behaviour of the flask application.

It decides:

    * The configuration level of the flask: Development, Testing or Production.
    * Loads each blueprint developed under the different sub-levels.
    * Initialize the database and makes the needed database session connections.
"""

import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

message = 'message'
# Load logging instance.
logger = logging.getLogger(__name__)

# Initializing SQLAlchemy
db = SQLAlchemy()

# Initialize app
app = Flask(__name__)

# Initialize jwt
jwt = JWTManager(app)

configuration_parameters = {
    'development': 'project.config.DevelopmentConfig',
    'testing': 'project.config.TestingConfig',
    'production': 'project.config.ProductionConfig',
}

def create_app():
    """
    Creates and configures an instance of the flask application
    :return: An app instance with the Flask application.
    """
    # Loads the configuration file. Defaults to development in case that RUN_MODE is not set.
    configuration = os.environ.get('RUN_MODE', 'production')
    app.config.from_object(configuration_parameters.get(configuration, 'production'))
    # initialize Flask-SQLAlchemy and the init-db command (makes logical connection Flask < -- > DB)
    db.init_app(app)
    # apply blueprints to the app. We can select what type of BPs we want to add
    from project import auth
    app.register_blueprint(auth.bp)
    from project import countries
    app.register_blueprint(countries.bp)
    return app


def init_db():
    """
    Drops all the tables and information of the current database and creates the tables structure.
    WARNING: this method will DESTROY YOUR DATA.
    :return: None
    """
    logger.info("Reloading database")
    logger.warning("The database is being reloaded. Old values where cleared")
    db.drop_all()
    db.create_all()
    logger.info("Database cleaned and initialized")


@app.before_first_request
def create_tables():
    """
    Create database tables if they are not created
    :return:
    """
    db.create_all()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    from project.auth import models
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.query.filter_by(jti=jti).first()

