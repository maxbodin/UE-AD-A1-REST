import json
import requests
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest, Conflict

from constants import BOOKING_PORT, HOST, SHOWTIME_PORT

app = Flask(__name__)

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


@app.route("/bookings", methods=['GET'])
def get_all_bookings():
    return jsonify(bookings), 200


@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    user_bookings = [booking for booking in bookings if booking['userid'] == userid]

    if user_bookings:
        return jsonify(user_bookings), 200
    else:
        return jsonify({"error": "No bookings found for the specified user"}), 404


@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_for_user(userid):
    new_booking = request.json
    booking_date = new_booking.get('date')
    booking_movieid = new_booking.get('movieid')

    # Validate the request body.
    if not booking_date or not booking_movieid:
        raise BadRequest("Invalid input: 'date' and 'movieid' are required.")

    # Check if the booking already exists.
    for booking in bookings:
        if booking['userid'] == userid:
            for date_entry in booking['dates']:
                if date_entry['date'] == booking_date and booking_movieid in date_entry['movies']:
                    raise Conflict("Booking already exists for this date and movie.")

    # Request the Showtime service to validate the movie for the specified date.
    try:
        showtime_response = requests.get(f'http://{HOST}:{SHOWTIME_PORT}/showmovies/{booking_date}')
        if showtime_response.status_code != 200:
            raise BadRequest(f"No valid showtime found for date {booking_date}")

        showtimes = showtime_response.json()
        valid_movie = any(booking_movieid in day['movies'] for day in showtimes)
        if not valid_movie:
            raise BadRequest(f"Movie ID {booking_movieid} is not valid for date {booking_date}")

    except requests.exceptions.RequestException as e:
        raise BadRequest(f"Error contacting the Showtime service: {str(e)}")

    # Add the booking for the user.
    for booking in bookings:
        if booking['userid'] == userid:
            for date_entry in booking['dates']:
                if date_entry['date'] == booking_date:
                    date_entry['movies'].append(booking_movieid)
                    break
            else:
                booking['dates'].append({"date": booking_date, "movies": [booking_movieid]})
            break
    else:
        bookings.append({"userid": userid, "dates": [{"date": booking_date, "movies": [booking_movieid]}]})

    write(bookings)

    return jsonify({"message": "Booking successfully created"}), 200


def write(all_bookings):
    with open('{}/databases/bookings.json'.format("."), 'w') as f:
        movies_dict = {'bookings': all_bookings}
        json.dump(movies_dict, f)


@app.route("/help", methods=['GET'])
def movie_help():
    endpoints = {
        "GET /": "Home page of the Booking service",
        "GET /bookings": "Get all the bookings",
        "GET /bookings/<userid>": "Get bookings for a specific user by their user ID",
        "POST /bookings/<userid>": "Add a booking for a user",
    }
    return jsonify(endpoints), 200


if __name__ == "__main__":
    print("Server running in port %s" % BOOKING_PORT)
    app.run(host=HOST, port=BOOKING_PORT)
