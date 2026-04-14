from flask import Flask, request, jsonify
import sys, os

sys.path.append(os.path.abspath("../src"))

from users import UserManager

app = Flask(__name__)
users = UserManager()

@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json

    users.add_user(
        data["name"],
        data["api_key"],
        data["api_secret"],
        data["balance"]
    )

    return jsonify({"status": "ok"})

@app.route("/users")
def get_users():
    return jsonify(users.get_users())

app.run(port=5000)