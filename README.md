# FlaskApi
# How to run

pip install -r requirements.txt

### Run at localhost:5000
python main.py

The output files generated with get requests will be set in the project/countries/output directory. There files have been commited.

The resource folder contains registros.csv file which is used to post at the localhost:5000/api/v1/upload endpoint.

### Run tests

python test_resources.py

### Download the docker image

docker pull docker.pkg.github.com/victordolado/flaskapi/flask-app:v1

### Run the docker image

docker run flask-app
