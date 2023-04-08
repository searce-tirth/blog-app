from pymongo import MongoClient
import certifi


def get_db_connection():
    ca = certifi.where()
    return MongoClient('mongodb+srv://tirth:D9ePj1pX14Yy6kCy@cluster0.4qezvaw.mongodb.net/?retryWrites=true&w=majority',
                       tlsCAFile=ca).internship
    # return MongoClient('mongodb://localhost:27017').internship
