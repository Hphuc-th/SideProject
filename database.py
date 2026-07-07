from pymongo import MongoClient
import json
import os

uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.5.6"
client = MongoClient(uri)

database = client.get_database("crawler")
posting = database.get_collection("posting")
movies = database.get_collection("movies")


