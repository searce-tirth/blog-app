import json
from flask_cors import CORS
from flask import Flask, Response, request, render_template
from view.create_blog import createBlog

from view.create_user import createUser
from view.read_blog import readBlog
from view.delete_blog import deleteBlog
from view.add_deleted_blog import adddeletedBlog

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['GET'])
def test():
    return render_template("readblog.html")


@app.route("/create_user", methods=['POST'])
def create_user():
    request_payload = request.get_json(force=True)
    process = createUser(request_payload=request_payload)
    return process.response


@app.route("/create_blog", methods=["POST"])
def create_blog():
    request_payload = request.get_json(force=True)
    process = createBlog(request_payload=request_payload)
    return process.response


@app.route("/read_blog", methods=["POST"])
def read_blog():
    request_payload = request.get_json(force=True)
    process = readBlog(request_payload=request_payload)
    return process.response


@app.route("/delete_blog", methods=["POST"])
def delete_blog():
    request_payload = request.get_json(force=True)
    process = deleteBlog(request_payload=request_payload)
    return process.response


@app.route("/add_deleted_blog", methods=["POST"])
def add_deleted_blog():
    request_payload = request.get_json(force=True)
    process = adddeletedBlog(request_payload=request_payload)
    return process.response


if __name__ == '__main__':
    app.run(port=80, host="0.0.0.0", debug=True)
