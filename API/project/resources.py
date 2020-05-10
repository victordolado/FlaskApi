import os
from flask_restful import Resource
from project import models
from flask_jwt_extended import (create_access_token, jwt_required, get_raw_jwt)
from flask import *
import csv
import requests
import pandas as pd
import weasyprint

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        user = models.UserModel.query.filter_by(username=data.get('username')).first()
        if user:
            return {'message': 'User {} already exists'.format(data.get('username')), "status code": 200}

        else:
            new_user = models.UserModel(
                username=data.get('username'),
                password=models.UserModel.generate_hash(data.get('password')),
                name=data.get('name'),
                surname=data.get('surname'),
                email=data.get('email'),
            )

            try:
                new_user.add()
                access_token = create_access_token(identity=data.get('username'))
                return {
                    'message': 'User {} was created'.format(data.get('username')),
                    'access_token': access_token,
                    'status code': 200
                }
            except Exception as e:
                return {'message': 'Something went wrong: {}'.format(e), 'status code': 500}


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        current_user = models.UserModel.query.filter_by(username=data.get('username')).first()

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data.get('username')), 'status code': 404}

        if (data.get("username")==current_user.username or data.get("email")==current_user.email) and models.UserModel.verify_hash(data.get('password'), current_user.password):
            access_token = create_access_token(identity=data.get('username'))
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'status code': 200
            }
        else:
            return {'message': 'Wrong credentials', 'status code': 401}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = models.RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked', 'status code': 200}
        except Exception as e:
            return {'message': 'Something went wrong: {}'.format(e), 'status code': 500}

class UploadCSVFile(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        csv_file = data.get("csv_file")
        with open(csv_file) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')  # todo es más sencillo con pandas.
            for row in csv_reader:
                username, password, name, surname, email = row
                user = models.UserModel(username=username, password=password, name=name, surname=surname, email=email)
                if models.UserModel.query.filter_by(username=username).first():
                    return {'message': 'User {} already exists'.format(username), 'status code': 200}

                else:

                    try:
                        user.add()
                        access_token = create_access_token(identity=username)
                        return {
                            'message': 'User {} was created'.format(username),
                            'access_token': access_token,
                            'status code': 200
                        }

                    except Exception as e:
                        return {'message': 'Something went wrong: {}'.format(e), 'status code': 500}


class GetPopulation(Resource):
    @jwt_required
    def get(self):
        try:
            data = requests.get("https://restcountries.eu/rest/v2/all")
            json_data = data.json()
            dict_population = dict()
            for json in json_data:
                dict_population[json["name"]] = json["population"]

            return {'countries and population':dict_population, 'status code': 200}

        except Exception as e:

            return {'message': 'Something went wrong: {}'.format(e), 'status code': 500}


class WriteCSV(Resource):
    @jwt_required
    def get(self):

        try:
            df = pd.DataFrame(columns=['name', 'capital', 'region', 'lat', 'long', 'population', 'alpha3Code'])
            data = requests.get("https://restcountries.eu/rest/v2/all")
            json_data = data.json()
            for i, json in enumerate(json_data):
                if json["latlng"]: #sometimes the list is empty
                    df.loc[i] = [json["name"], json["capital"], json["region"], json["latlng"][0], json["latlng"][1], json["population"], json["alpha3Code"]]
                else:
                    df.loc[i] = [json["name"], json["capital"], json["region"], None, None, json["population"], json["alpha3Code"]]

            output_path = os.path.join(os.path.dirname(str(__file__)), "output", "countries.csv")
            df.to_csv(output_path, sep=',', encoding='utf-8')

            return {'message': 'The file has been written', 'output path': output_path, 'status code': 200}

        except Exception as e:

            return {'message': 'Something went wrong: {}'.format(e), 'status code': 500}


class WritePDF(Resource):
    @jwt_required
    def get(self):
        try:
            df = pd.DataFrame(columns=['name', 'capital', 'region', 'lat', 'long', 'population', 'alpha3Code'])
            data = requests.get("https://restcountries.eu/rest/v2/all")
            json_data = data.json()

            for i, json in enumerate(json_data):
                if json["latlng"]: #sometimes the list is empty
                    df.loc[i] = [json["name"], json["capital"], json["region"], json["latlng"][0], json["latlng"][1], json["population"], json["alpha3Code"]]
                else:
                    df.loc[i] = [json["name"], json["capital"], json["region"], None, None, json["population"], json["alpha3Code"]]

            output_html = os.path.join(os.path.dirname(str(__file__)), 'output', 'countries.html')
            self.to_html_pretty(df, output_html)
            output_path = os.path.join(os.path.dirname(str(__file__)), "output", "countries.pdf")
            weasyprint.HTML(output_html).write_pdf(output_path)

            return {'message': 'The pdf has been written','output path': output_path, 'status code': 200}


        except Exception as e:

            return {'message': 'Something went wrong: {}'.format(e), 'status code': 500}


    def to_html_pretty(self, df, filename, title='COUNTRIES INFORMATION'):
        '''
        Write an entire dataframe to an HTML file with nice formatting.
        '''
        HTML_TEMPLATE1 = '''
                    <html>
                    <head>
                    <style>
                      h2 {
                        text-align: center;
                        font-family: Helvetica, Arial, sans-serif;
                      }
                      table { 
                        margin-left: auto;
                        margin-right: auto;
                      }
                      table, th, td {
                        border: 1px solid black;
                        border-collapse: collapse;
                      }
                      th, td {
                        padding: 5px;
                        text-align: center;
                        font-family: Helvetica, Arial, sans-serif;
                        font-size: 90%;
                      }
                      table tbody tr:hover {
                        background-color: #dddddd;
                      }
                      .wide {
                        width: 90%; 
                      }

                    </style>
                    </head>
                    <body>
                    '''

        HTML_TEMPLATE2 = '''
                    </body>
                    </html>
                    '''
        ht = ''
        if title != '':
            ht += '<h2> %s </h2>\n' % title
        ht += df.to_html(classes='wide', escape=False)

        with open(filename, 'w') as f:
            f.write(HTML_TEMPLATE1 + ht + HTML_TEMPLATE2)