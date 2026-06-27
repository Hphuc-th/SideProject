from pymongo import MongoClient
import json
import os
import mon

uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.5.6"
client = MongoClient(uri)

try:
    database = client.get_database("sample_mflix")
    movies = database.get_collection("movies")

    # Queries for a movie that has the title 'Back to the Future'
    query = { "title": "Back to the Future" }


except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)


