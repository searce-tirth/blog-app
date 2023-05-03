import datetime
import json

from flask import Response

from utilities.get_db_connection import get_db_connection
import string
import random


class createUser:
    def __init__(self, name,dob,gender):
        
        self.NAME = name
        self.DOB = dob
        self.GENDER = gender
        self.response = Response(
            json.dumps({
                "message":"Internal Server Error"
            }),status=500,mimetype="application/json"
        )

        self.main()

    def main(self):
        self.get_db_connection()
        self.create_user()
        self.persist_to_db()
        self.response = Response(json.dumps({
            "message": "Created User",
            "data":{
                "user_id": self.ID
            },
        }), status=200, mimetype="application/json")

    def get_db_connection(self):
        self.response = Response( json.dumps({
                "message":"Can't connect to Database"
            }),status=500,mimetype="application/json")
        self.DB_CONNECTION = get_db_connection().sample

    def create_user(self):
        self.response = Response(json.dumps({
            "message": "Can't create the user"
        }), status=500, mimetype="application/json")
        self.ID = ''.join(random.choices(string.ascii_uppercase +
                                         string.digits, k=12))
        self.CREATED_AT = datetime.datetime.now()
        self.user = {
            'id': self.ID,
            "name": self.NAME,
            "dob": self.DOB,
            "gender": self.GENDER,
            "blogs": [],
            #"saved": [],
            "created_at": self.CREATED_AT
        }

    def persist_to_db(self):
        self.response = Response(json.dumps({
            "message": "Unable to persist data"
        }), status=500, mimetype="application/json")
        self.DB_CONNECTION.insert_one(self.user)
