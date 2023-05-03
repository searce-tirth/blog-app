import json
import random
from flask import Response
from utilities.get_db_connection import get_db_connection

list1=[]
class getrandomBlogs:
    def __init__(self):
        
        
        
        self.response = Response(
            json.dumps({
                "message": "Internal Server Error"
            }), status=500, mimetype="application/json"
        )

        self.main()

    def main(self):
        list1.clear()
        self.get_db_connection()
        self.read_from_db()

        # self.persist_to_db()
        try:
            self.response = Response(json.dumps({
                "message": "Read Blog",
                "data": list1,
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
        num_docs = self.DB_CONNECTION.count_documents({})

        # generate a list of random indices
        rand_indices = random.sample(range(num_docs), k=20)
        dictn = (self.DB_CONNECTION.aggregate([{ '$sample': { 'size': 20 }}]))
        print(type(dictn))
        
        c=0
        for i in dictn:
            for j in i["blogs"]:
                if j["delete_status"] == "false":
                    self.BLOG_NAME = j["blog_name"]
                    self.CONTENT = j["content"]
                    self.CREATED_AT = str(j["created_at"])
                    self.VIEW = j["views"]
                    self.add_viewer_count()
                    list1.append({"data": {
                    "blog_name": self.BLOG_NAME,
                    "content": self.CONTENT,
                    "createdAt": self.CREATED_AT,
                    "views": self.VIEW
                }})
                    
                    break
                elif j["delete_status"] == "true":
                    print("this is deleted")
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
