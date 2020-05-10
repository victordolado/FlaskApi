import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(str(__file__))))
from project.models import db
from project.run import app
import json

class TestResources(unittest.TestCase):

    def setUp(self):

        app.testing = True
        self.client = app.test_client()

        self.username = "Victor"
        self.email = "victor@gmail.com"
        self.password = "pass"
        self.name = "Victor"
        self.surname = "Dolado"
        self.general_payload = json.dumps({
            "email": self.email,
            "password": self.password,
            "username": self.username,
            "name": self.name,
            "surname": self.surname
        })

    def test_successful_signup(self):

        response = self.client.post('/api/v1/signup', headers={"Content-Type": "application/json"}, data=self.general_payload)
        self.assertEqual(200, response.json["status code"])

    def test_already_signup(self):

        self.client.post('/api/v1/signup', headers={"Content-Type": "application/json"}, data=self.general_payload)
        response= self.client.post('/api/v1/signup', headers={"Content-Type": "application/json"}, data=self.general_payload)

        self.assertIn("already", response.json['message'])
        self.assertEqual(200, response.json["status code"])

    def test_successful_signin(self):

        self.client.post('/api/v1/signup', headers={"Content-Type": "application/json"}, data=self.general_payload)
        response = self.client.post('/api/v1/signin', headers={"Content-Type": "application/json"}, data=self.general_payload)

        self.assertEqual(200, response.json["status code"])

    def test_wrong_credentials_signin(self):

        username = "Victor"
        email = "victor@gmail.com"
        password = "incorrect_pass"
        name = "Victor"
        surname = "Dolado"
        payload = json.dumps({
            "email": email,
            "password": password,
            "username": username,
            "name": name,
            "surname": surname
        })

        self.client.post('/api/v1/signup', headers={"Content-Type": "application/json"}, data=self.general_payload)
        response = self.client.post('/api/v1/signin', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(401, response.json["status code"])

    def test_not_user_signin(self):

        username="Marcos"
        email = "marcos@gmail.com"
        password = "pass"
        name = "Marcos"
        surname = "Dolado"

        payload = json.dumps({
            "email": email,
            "password": password,
            "username": username,
            "name": name,
            "surname": surname
        })

        response = self.client.post('/api/v1/signin', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(404, response.json["status code"])

    def test_successful_logout(self):

        self.client.post('/api/v1/signup', headers={"Content-Type": "application/json"}, data=self.general_payload)

        response_signin = self.client.post('/api/v1/signin', headers={"Content-Type": "application/json"}, data=self.general_payload)
        access_token = response_signin.json["access_token"]

        response = self.client.post('/api/v1/signout', headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(access_token)}, data=self.general_payload)

        self.assertEqual(200, response.json["status code"])

    def test_successful_upload(self):

        csv_file = os.path.join(os.path.dirname(__file__), "resources", "registros.csv")

        payload = json.dumps({
            "csv_file": csv_file
        })

        self.client.post('/api/v1/signup', headers={"Content-Type": "application/json"}, data=self.general_payload)

        response_signin = self.client.post('/api/v1/signin', headers={"Content-Type": "application/json"}, data=self.general_payload)
        access_token = response_signin.json["access_token"]

        response = self.client.post('/api/v1/upload', headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(access_token)}, data=payload)
        self.assertEqual(200, response.json["status code"])

    def test_successful_population(self):

        self.client.post('/api/v1/signup', headers={"Content-Type": "application/json"}, data=self.general_payload)

        response_signin = self.client.post('/api/v1/signin', headers={"Content-Type": "application/json"}, data=self.general_payload)
        access_token = response_signin.json["access_token"]

        response = self.client.get('/api/v1/countries/population', headers={"Content-Type": "application/json",
                                                                      "Authorization": "Bearer {}".format(
                                                                          access_token)})

        self.assertEqual(200, response.json["status code"])

    def test_successful_writeCSV(self):

        self.client.post('/api/v1/signup', headers={"Content-Type": "application/json"}, data=self.general_payload)

        response_signin = self.client.post('/api/v1/signin', headers={"Content-Type": "application/json"}, data=self.general_payload)
        access_token = response_signin.json["access_token"]

        response = self.client.get('/api/v1/countries/csv', headers={"Content-Type": "application/json",
                                                                      "Authorization": "Bearer {}".format(
                                                                          access_token)})

        self.assertEqual(200, response.json["status code"])


    def test_successful_writePDF(self):


        self.client.post('/api/v1/signup', headers={"Content-Type": "application/json"}, data=self.general_payload)

        response_signin = self.client.post('/api/v1/signin', headers={"Content-Type": "application/json"}, data=self.general_payload)
        access_token = response_signin.json["access_token"]

        response = self.client.get('/api/v1/countries/pdf', headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(
                                                                          access_token)})

        self.assertEqual(200, response.json["status code"])


if __name__=="__main__":

    unittest.main()
