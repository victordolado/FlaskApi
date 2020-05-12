# APIs using Python, Flask and SQLAlchemy.

## APIs

### Registration

  * **URL**: /api/v1/signup
  * **Input**: Username, Password, Name, Surname, Email
  * **Example**: {"username" : "victor", "password" : "pass", "name" : "Victor", "surname" : "Dolado", "email" : "victor@gmail.com"}

### Login (JWT)

  * **URL**: /api/v1/signin
  * **Input**: Username or email, Password
  * **Example**: {"username" : "victor", "password" : "pass", "email" : "victor@gmail.com"}

### Logout (JWT) - Revoke token

  * **URL**: /api/v1/logout
  * **PRE**: Needs login
  * **Input**: Username or email Password
  * **Example**: {"username" : "victor", "password" : "pass", "email" : "victor@gmail.com"}
 
### Load csv file:

  * **URL**: /api/v1/upload
  * **PRE**: Needs login
  * **Input**: csv file
  * **CSV file format**: resources/registros.csv
 
 ### External API, call to (call to https://restcountries.eu/rest/v2/all):
 
  * **URL**: /api/v1/countries/population
  * **PRE**: Needs login
  * **Return**: 
    { 
     "countries and population":{
        "country_name": "population"
        }
    }
  
  
 ### External API, Create CSV file with the next columns (call to https://restcountries.eu/rest/v2/all):
  
  * **URL**: /api/v1/countries/csv
  * **PRE**: Needs login
  * **CSV FIELDS**:
      * name
      * capital
      * region
      * lat
      * long
      * population
      * alpha3Code
  * **Example**: project/countries/output/countries.csv
 
 ### External API, Create PDF file with the next columns in a table (call to https://restcountries.eu/rest/v2/all):
  
  * **URL**: /api/v1/countries/pdf
  * **PRE**: Needs login
  * **TABLE FIELDS**:
      * name
      * capital
      * region
      * lat
      * long
      * population
      * alpha3Code
  * **Example**: project/countries/output/countries.pdf
 
# How to run

    pip install -r requirements.txt

### Run at localhost:5000
  
    python main.py

The output files generated with get requests will be set in the project/countries/output directory.

### Run tests

    python test_resources.py

### Download the docker image

    docker pull docker.pkg.github.com/victordolado/flaskapi/flask-app:v1

### Run the docker image

    docker run flask-app
