from pymongo import MongoClient
import json
import os

uri = "mongodb://172.17.128.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.5.6"
client = MongoClient(uri)
database = client.get_database("crawler")


def get_posting():
    return database.get_collection("posting")


def close_db():
    client.close()
