import json
from flask import Flask, jsonify
from constants import HOST, SHOWTIME_PORT

app = Flask(__name__)

with open('{}/databases/times.json'.format("."), "r") as jsf:
    schedule = json.load(jsf)["schedule"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"


@app.route("/showtimes", methods=['GET'])
def get_schedule():
    return jsonify(schedule), 200


@app.route("/showmovies/<date>", methods=['GET'])
def get_movies_bydate(date):
    result = [entry for entry in schedule if entry.get('date') == date]

    if result:
        return jsonify(result), 200
    else:
        return jsonify({"error": "No schedule found for the specified date"}), 404


@app.route("/help", methods=['GET'])
def showtime_help():
    endpoints = {
        "GET /": "Home page of the Showtime service",
        "GET /showtimes": "Get the full showtime schedule.",
        "GET /showmovies/<date>": "Get the showtime schedule for a specific date.",
    }
    return jsonify(endpoints), 200


if __name__ == "__main__":
    print("Server running in port %s" % SHOWTIME_PORT)
    app.run(host=HOST, port=SHOWTIME_PORT)
