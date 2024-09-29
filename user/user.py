import json

from flask import Flask

from constants import HOST, USER_PORT

app = Flask(__name__)

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


if __name__ == "__main__":
    print("Server running in port %s" % USER_PORT)
    app.run(host=HOST, port=USER_PORT)
