import json
from flask_cors import CORS
from flask import Flask, Response, jsonify, request, render_template
from view.create_blog import createBlog

from view.create_user import createUser
from view.read_blog import readBlog
from view.delete_blog import deleteBlog
from view.add_deleted_blog import adddeletedBlog
from view.get_random_blogs import getrandomBlogs

app = Flask(__name__)
CORS(app)
app.secret_key = 'some_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config['random'] = ""
def clearfunc():
    #Global variables
    
    app.config['response']=""
    app.config['code']=""
    app.config['status'] = ""
    
    
    
    
#modify app.config for first time
clearfunc()

@app.route("/", methods=['GET'])
def test():
    return render_template("index.html")


@app.route("/create_user", methods=['POST'])
def create_user():
    clearfunc()
    name = request.form["name"]
    dob = request.form["dob"]
    gender = request.form["gender"]
    process = createUser(name,dob,gender)
    app.config['response']=process.response
    app.config['code']=0
    app.config['status']="Completed"
    return '',204


@app.route("/create_blog", methods=["POST"])
def create_blog():
    clearfunc()
    id = request.form["id"]
    name = request.form["name"]
    content = request.form["content"]
    process = createBlog(id,name,content)
    app.config['response']=process.response
    app.config['code']=1
    app.config['status']="Completed"
    return '',204


@app.route("/read_blog", methods=["POST"])
def read_blog():
    clearfunc()
    name = request.form["blogName"]
    process = readBlog(name)
    app.config['response']=process.response
    app.config['code']=2
    app.config['status']="Completed"
    return '',204


@app.route("/delete_blog", methods=["POST"])
def delete_blog():
    clearfunc()
    uname = request.form["uname"]
    uid = request.form["uid"]
    bname = request.form["bname"]
    process = deleteBlog(uid,uname,bname)
    app.config['response']=process.response
    app.config['code']=3
    app.config['status']="Completed"
    return '',204


@app.route("/add_deleted_blog", methods=["POST"])
def add_deleted_blog():
    clearfunc()
    uname = request.form["uname"]
    uid = request.form["uid"]
    bname = request.form["bname"]
    process = adddeletedBlog(uid,uname,bname)
    app.config['response']=process.response
    app.config['code']=4
    app.config['status']="Completed"
    return '',204


@app.route("/process", methods=["GET"])
def process():
    while(app.config['status'] != "Completed"):
        continue
    
    response = app.config['response']
    json_data = json.loads(response.get_data())
    print(json_data)
    newData = {"code": app.config['code']}
    json_data.update(newData)
    clearfunc()
    return jsonify(json_data)

@app.route("/sample", methods=["GET"])
def sample():
    app.config['random']=""
    process = getrandomBlogs()
    app.config['random'] = process.response
    json_data = json.loads(app.config['random'].get_data())
    print(json_data)
    
    return jsonify(json_data)

if __name__ == '__main__':
    app.run(port=80, host="0.0.0.0", debug=True)
