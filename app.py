from flask import Flask, jsonify, request
from database import movies

app = Flask(__name__)

@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/movies", methods=["GET"])
def get_movies():
    breakpoint()
    query = {}
    for field in ["title", "year", "genres", "director"]:
        val = request.args.get(field)
        if val:
            if field == "year":
                query[field] = int(val)
            else:
                query[field] = val

    results = list(movies.find(query).limit(10))
    for r in results:
        r["_id"] = str(r["_id"])
    return jsonify(results)

@app.route("/movies/count",methods=["GET"])
def get_movies_count():
    count = movies.count_documents({})
    return jsonify({"count": count})