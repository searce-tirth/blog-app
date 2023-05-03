import datetime
import json

from flask import Response

from utilities.get_db_connection import get_db_connection
import string
import random


class createBlog:
    def __init__(self, id,name,content):
        
        self.USER_ID = id
        self.BLOG_NAME = name
        self.CONTENT = content
        

        self.response = Response(
            json.dumps({
                "message":"Internal Server Error"
            }),status=500,mimetype="application/json"
        )

        self.main()

    def main(self):
        self.get_db_connection()
        self.create_blog()
        self.persist_to_db()
        self.response = Response(json.dumps({
            "message": "Created Blog",
            "data":{
                "user_id": self.USER_ID,
                "blog_id": self.ID,
                "blog_name": self.BLOG_NAME,
                "content": self.CONTENT
            },
        }), status=200, mimetype="application/json")

    def get_db_connection(self):
        self.response = Response( json.dumps({
                "message":"Can't connect to Database"
            }),status=500,mimetype="application/json")
        self.DB_CONNECTION = get_db_connection().sample

    def create_blog(self):
        self.response = Response(json.dumps({
            "message": "Can't create the blog"
        }), status=500, mimetype="application/json")
        self.ID = ''.join(random.choices(string.ascii_uppercase +
                                         string.digits, k=12))
        self.CREATED_AT = datetime.datetime.now()
        self.blog = {
            'blog_id': self.ID,
            "blog_name": self.BLOG_NAME,
            "content": self.CONTENT,
            "created_at": self.CREATED_AT,
            "delete_status" : "false",
            "views": 0
        }

    def persist_to_db(self):
        self.response = Response(json.dumps({
            "message": "Unable to persist data"
        }), status=500, mimetype="application/json")
        #dict = list(self.DB_CONNECTION.find({"id" : str(self.USER_ID)},{"blogs":1,"_id":0}))
        #dict.append(self.blog)
        self.DB_CONNECTION.update_one({"id" : str(self.USER_ID)}, {"$push":{"blogs":self.blog}})
