import sys
import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
sys.path.insert(0, os.path.join(os.path.dirname(str(__file__))))
import resources
import models

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '{\xb9\xe1]0\x87\x96\x9aN\xa1)\xa2W\x1b]2\xc1T%:\xc7En\x9e'

db = SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = 'qwertyuiopasdfghjklzxcvbnm123456'
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

@app.before_first_request
def create_tables():
    db.create_all()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.query.filter_by(jti=jti).first()


api.add_resource(resources.UserRegistration, '/api/v1/signup')
api.add_resource(resources.UserLogin, '/api/v1/signin')
api.add_resource(resources.UserLogoutAccess, '/api/v1/signout')
api.add_resource(resources.UploadCSVFile, '/api/v1/upload')
api.add_resource(resources.GetPopulation, '/api/v1/countries/population')
api.add_resource(resources.WriteCSV, '/api/v1/countries/csv')
api.add_resource(resources.WritePDF, '/api/v1/countries/pdf')