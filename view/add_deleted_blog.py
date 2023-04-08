import json
from flask import Response
from utilities.get_db_connection import get_db_connection



class adddeletedBlog:
    def __init__(self, request_payload):
        self.request_payload = request_payload
        self.USER_ID = self.request_payload.get("user_id")
        self.BLOG_ID = self.request_payload.get("blog_id")
        

        self.response = Response(
            json.dumps({
                "message":"Internal Server Error"
            }),status=500,mimetype="application/json"
        )

        self.main()

    def main(self):
        self.get_db_connection()
        self.add_deleted_from_db()
        
        #self.persist_to_db()
        try:
            self.response = Response(json.dumps({
                "message": "Added Deleted Blog",
                "data" : {
                    "blog_id":self.BLOG_ID,
                    "content":self.CONTENT
                }
            }), status=200, mimetype="application/json")
        except:
            pass

    def get_db_connection(self):
        self.response = Response( json.dumps({
                "message":"Can't connect to Database"
            }),status=500,mimetype="application/json")
        self.DB_CONNECTION = get_db_connection().sample

    def add_deleted_from_db(self):
        self.response = Response(json.dumps({
            "message": "Can't delete the blog from Database"
        }), status=500, mimetype="application/json")
        dictn = (self.DB_CONNECTION.find({"id" : str(self.USER_ID)},{"blogs":1,"_id":0}))
        for i in dictn:
            for j in i["blogs"]:
                if j["blog_id"] == (self.BLOG_ID) and j["delete_status"] == "true":
                    self.CONTENT = j["content"]
                    self.CREATED_AT = str(j["created_at"])
                    self.add_deleted_blog()
                    return
                
                elif j["blog_id"] == (self.BLOG_ID) and j["delete_status"] == "false":
                    self.response = Response(json.dumps({
                    "message": "Blog is not deleted"
                    }), status=500, mimetype="application/json")
                    return
            else:
                self.response = Response(json.dumps({
                    "message": "You can't add this deleted blog"
                }), status=500, mimetype="application/json")
                break
            
        else:
            self.response = Response(json.dumps({
                    "message": "User doesn't exist"
                }), status=500, mimetype="application/json")
            
    def add_deleted_blog(self):
        self.response = Response(json.dumps({
            "message": "Can't get the blog from Database"
        }), status=500, mimetype="application/json")
        self.DB_CONNECTION.update_one({"id" : str(self.USER_ID),"blogs.blog_id":str(self.BLOG_ID)}, {"$set" : {"blogs.$.delete_status" : "false"}})
        
                


    
