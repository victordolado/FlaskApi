import os
import logging
import requests
import pandas as pd
from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required
import weasyprint
message = 'message'
logger = logging.getLogger(__name__)

# Registering blueprint of this module
bp = Blueprint("countries", __name__, url_prefix="/api/v1/countries")

@bp.route("/population", methods=['GET'])
@jwt_required
def get_population():
    try:
        data = requests.get("https://restcountries.eu/rest/v2/all")
        json_data = data.json()
        dict_population = dict()
        for json in json_data:
            dict_population[json["name"]] = json["population"]

        return jsonify({'countries and population':dict_population}), 200

    except Exception as e:
        logger.error("Error in get_population(): {}".format(e))
        return jsonify({message: 'Something went wrong: {}'.format(e)}), 500

@bp.route("/csv", methods=['GET'])
@jwt_required
def get_csv():
    try:
        df = pd.DataFrame(columns=['name', 'capital', 'region', 'lat', 'long', 'population', 'alpha3Code'])
        data = requests.get("https://restcountries.eu/rest/v2/all")
        json_data = data.json()
        for i, json in enumerate(json_data):
            if json["latlng"]:  # sometimes the list is empty
                df.loc[i] = [json["name"], json["capital"], json["region"], json["latlng"][0], json["latlng"][1],
                             json["population"], json["alpha3Code"]]
            else:
                df.loc[i] = [json["name"], json["capital"], json["region"], None, None, json["population"],
                             json["alpha3Code"]]
        output_dir = os.path.join(os.path.dirname(str(__file__)), "output")

        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "countries.csv")
        df.to_csv(output_path, sep=',', encoding='utf-8')

        return jsonify({message: 'The file has been written', 'output path': output_path}), 200

    except Exception as e:
        logger.error("Error in get_csv(): {}".format(e))
        return jsonify({message: f'Something went wrong'}), 500

@bp.route("/pdf", methods=['GET'])
@jwt_required
def get_pdf():
    try:
        df = pd.DataFrame(columns=['name', 'capital', 'region', 'lat', 'long', 'population', 'alpha3Code'])
        data = requests.get("https://restcountries.eu/rest/v2/all")
        json_data = data.json()

        for i, json in enumerate(json_data):
            if json["latlng"]: #sometimes the list is empty
                df.loc[i] = [json["name"], json["capital"], json["region"], json["latlng"][0], json["latlng"][1], json["population"], json["alpha3Code"]]
            else:
                df.loc[i] = [json["name"], json["capital"], json["region"], None, None, json["population"], json["alpha3Code"]]

        output_dir =  os.path.join(os.path.dirname(str(__file__)), 'output')
        os.makedirs(output_dir, exist_ok=True)

        output_html = os.path.join(output_dir, 'countries.html')
        to_html_pretty(df, output_html)
        output_path = os.path.join(output_dir, 'countries.pdf')
        weasyprint.HTML(output_html).write_pdf(output_path)

        return jsonify({'message': 'The pdf has been written','output path': output_path}), 200


    except Exception as e:
        logger.error("Error in get_pdf(): {}".format(e))
        return jsonify({'message': 'Something went wrong: {}'.format(e)}), 500


def to_html_pretty(df, filename, title='COUNTRIES INFORMATION'):
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