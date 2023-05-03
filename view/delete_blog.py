import json
from flask import Response
from utilities.get_db_connection import get_db_connection



class deleteBlog:
    def __init__(self, uid,uname,bname):
        
        self.USER_NAME = uname
        self.USER_ID = uid
        self.BLOG_NAME = bname
        

        self.response = Response(
            json.dumps({
                "message":"Internal Server Error"
            }),status=500,mimetype="application/json"
        )

        self.main()

    def main(self):
        self.get_db_connection()
        self.delete_from_db()
        
        #self.persist_to_db()
        # try:
        #     self.response = Response(json.dumps({
        #         "message": "Deleted Blog",
                
        #     }), status=200, mimetype="application/json")
        # except:
        #     pass

    def get_db_connection(self):
        self.response = Response( json.dumps({
                "message":"Can't connect to Database"
            }),status=500,mimetype="application/json")
        self.DB_CONNECTION = get_db_connection().sample

    def delete_from_db(self):
        self.response = Response(json.dumps({
            "message": "Can't delete the blog from Database"
        }), status=500, mimetype="application/json")
        dictn = (self.DB_CONNECTION.find({"id" : str(self.USER_ID)},{"blogs":1,"_id":0}))
        for i in dictn:
            for j in i["blogs"]:
                #print(j["blog_id"])
                if j["blog_name"] == (self.BLOG_NAME) and j["delete_status"] == "false":
                    self.CONTENT = j["content"]
                    self.CREATED_AT = str(j["created_at"])
                    self.delete_blog()
                    return
                
                elif j["blog_name"] == (self.BLOG_NAME) and j["delete_status"] == "true":
                    self.response = Response(json.dumps({
                    "message": "Blog is removed by author"
                    }), status=500, mimetype="application/json")
                    return
            else:
                self.response = Response(json.dumps({
                    "message": "Unauthorized user ID"
                }), status=500, mimetype="application/json")
                break
            
        else:
            self.response = Response(json.dumps({
                    "message": "Incorrect user ID"
                }), status=500, mimetype="application/json")
            
    def delete_blog(self):
        self.response = Response(json.dumps({
            "message": "Can't get the blog from Database"
        }), status=500, mimetype="application/json")
        self.DB_CONNECTION.update_one({"id" : str(self.USER_ID),"blogs.blog_name":str(self.BLOG_NAME)}, {"$set" : {"blogs.$.delete_status" : "true"}})
        
                


    
