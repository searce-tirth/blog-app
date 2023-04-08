import json
from flask import Response
from utilities.get_db_connection import get_db_connection


class readBlog:
    def __init__(self, request_payload):
        self.request_payload = request_payload
        self.USER_ID = self.request_payload.get("user_id")
        self.BLOG_ID = self.request_payload.get("blog_id")

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
                    "user_id": self.USER_ID,
                    "blog_id": self.BLOG_ID,
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
        dictn = (self.DB_CONNECTION.find({"id": str(self.USER_ID)}, {"blogs": 1, "_id": 0}))
        print(dictn)
        for i in dictn:
            for j in i["blogs"]:
                if j["blog_id"] == str(self.BLOG_ID) and j["delete_status"] == "false":
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
        self.DB_CONNECTION.update_one({"id": str(self.USER_ID), "blogs.blog_id": str(self.BLOG_ID)},
                                      {"$inc": {"blogs.$.views": 1}})
