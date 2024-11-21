import json
from flask import Flask, render_template, request, jsonify, make_response

from constants import MOVIE_PORT, HOST

app = Flask(__name__)

with open('{}/databases/movies.json'.format("."), 'r') as jsf:
    movies = json.load(jsf)["movies"]


# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)


@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'), 200)


@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res


@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie), 200)
            return res
    return make_response(jsonify({"error": "Movie ID not found"}), 400)


@app.route("/moviesbytitle/exact", methods=['GET'])
def get_movie_bytitle_exact():
    title = request.args.get('title', None)
    if title:
        result = [movie for movie in movies if movie.get('title') == title]
        if result:
            return jsonify(result), 200
        else:
            return jsonify({"error": "No movies found for the specified title"}), 404
    return jsonify({"error": "Title not provided"}), 400


@app.route("/moviesbytitle/contains", methods=['GET'])
def get_movie_bytitle_contains():
    title = request.args.get('title', None)
    if title:
        result = [movie for movie in movies if title.lower() in movie.get('title', '').lower()]
        if result:
            return jsonify(result), 200
        else:
            return jsonify({"error": "No movies found for the specified title"}), 404
    return jsonify({"error": "Title not provided"}), 400


@app.route("/moviesbydirector", methods=['GET'])
def get_movies_bydirector():
    director_name = request.args.get('director', None)
    if director_name:
        result = [movie for movie in movies if movie.get('director') == director_name]
        if result:
            return jsonify(result), 200
        else:
            return jsonify({"error": "No movies found for the specified director"}), 404
    return jsonify({"error": "Director name not provided"}), 400


@app.route("/moviesbygenre", methods=['GET'])
def get_movies_bygenre():
    genre = request.args.get('genre', None)
    if genre:
        result = [movie for movie in movies if genre in movie.get('genre', [])]
        if result:
            return jsonify(result), 200
        else:
            return jsonify({"error": "No movies found for the specified genre"}), 404
    return jsonify({"error": "Genre not provided"}), 400


@app.route("/addmovie/<movieid>", methods=['POST'])
def add_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error": "movie ID already exists"}), 409)

    movies.append(req)
    write(movies)
    res = make_response(jsonify({"message": "movie added"}), 200)
    return res


def write(all_movies):
    with open('{}/databases/movies.json'.format("."), 'w') as f:
        movies_dict = {'movies': all_movies}
        json.dump(movies_dict, f)


@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = rate
            write(movies)
            res = make_response(jsonify(movie), 200)
            return res

    res = make_response(jsonify({"error": "movie ID not found"}), 201)
    return res


@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            write(movies)
            return make_response(jsonify(movie), 200)

    res = make_response(jsonify({"error": "movie ID not found"}), 400)
    return res


@app.route("/help", methods=['GET'])
def movie_help():
    endpoints = {
        "GET /": "Home page of the Movie service",
        "GET /json": "Get the full JSON database",
        "GET /movies/<movieid>": "Get a movie by its ID",
        "GET /moviesbytitle?title=<title>": "Get a movie by its title",
        "GET /moviesbydirector?director=<director>": "Get movies by director",
        "GET /moviesbygenre?genre=<genre>": "Get movies by genre",
        "POST /addmovie/<movieid>": "Add a new movie (POST)",
        "PUT /movies/<movieid>/<rate>": "Update movie rating (PUT)",
        "DELETE /movies/<movieid>": "Delete a movie by its ID (DELETE)"
    }
    return jsonify(endpoints), 200


if __name__ == "__main__":
    print("Server running in port %s" % MOVIE_PORT)
    app.run(host=HOST, port=MOVIE_PORT)
