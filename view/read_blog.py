import json
from flask import Response
from utilities.get_db_connection import get_db_connection


class readBlog:
    def __init__(self, name):
        
        self.BLOG_NAME = name
        self.response = Response(
            json.dumps({
                "message": "Internal Server Error"
            }), status=500, mimetype="application/json"
        )

        self.main()

    def main(self):
        self.get_db_connection()
        self.read_from_db()

        # self.persist_to_db()
        try:
            self.response = Response(json.dumps({
                "message": "Read Blog",
                "data": {
                    "blog_name": self.BLOG_NAME,
                    "content": self.CONTENT,
                    "createdAt": self.CREATED_AT,
                    "views": self.VIEW
                },
            }), status=200, mimetype="application/json")
        except:
            pass

    def get_db_connection(self):
        self.response = Response(json.dumps({
            "message": "Can't connect to Database"
        }), status=500, mimetype="application/json")
        self.DB_CONNECTION = get_db_connection().sample

    def read_from_db(self):
        self.response = Response(json.dumps({
            "message": "Can't get the blog from Database"
        }), status=500, mimetype="application/json")
        dictn = (self.DB_CONNECTION.find({"blogs.blog_name": str(self.BLOG_NAME) },{"blogs": 1, "_id": 0}))
        print(type(dictn))
        for i in dictn:
            for j in i["blogs"]:
                if j["blog_name"] == str(self.BLOG_NAME) and j["delete_status"] == "false":
                    self.CONTENT = j["content"]
                    self.CREATED_AT = str(j["created_at"])
                    self.VIEW = j["views"]
                    self.add_viewer_count()
                    break
                elif j["delete_status"] == "true":
                    self.response = Response(json.dumps({
                        "message": "Blog is removed by author"
                    }), status=500, mimetype="application/json")
                    break
            else:
                self.response = Response(json.dumps({
                    "message": "Blog doesn't exist"
                }), status=500, mimetype="application/json")
                break
        else:
            self.response = Response(json.dumps({
                "message": "User doesn't exist"
            }), status=500, mimetype="application/json")

    def add_viewer_count(self):
        self.response = Response(json.dumps({
            "message": "Can't get the blog from Database"
        }), status=500, mimetype="application/json")
        self.DB_CONNECTION.update_one({"blogs.blog_name": str(self.BLOG_NAME)},
                                      {"$inc": {"blogs.$.views": 1}})
