from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Friend
from database import init_db
from flasgger import Swagger
import yaml

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
init_db(app)

# Add Swagger configuration
with open("user_service_swagger.yml", "r") as f:
    swagger_template = yaml.safe_load(f)
swagger = Swagger(app, template=swagger_template)


@app.route('/users/', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return {"error": "username and password are required"}, 400

    if User.query.filter_by(username=username).first():
        return {"error": "Username already exists"}, 409

    user = User(username=username)
    user.set_password(password)  # Hash the password

    db.session.add(user)
    db.session.commit()
    return {"message": "User created", "user_id": user.id}, 201


@app.route('/users/<int:user_id>/friends/', methods=['POST'])
def add_friend(user_id):
    data = request.json
    friend_id = data.get('friend_id')

    if not friend_id:
        return {"error": "friend_id is required"}, 400

    user = User.query.get(user_id)
    friend = User.query.get(friend_id)

    if not user or not friend:
        return {"error": "User or friend not found"}, 404

    if user_id == friend_id:
        return {"error": "Cannot add yourself as a friend"}, 400

    existing = Friend.query.filter_by(user_id=user_id, friend_id=friend_id).first()
    if existing:
        return {"message": "Already friends"}, 200

    # Add bidirectional friendship
    friendship1 = Friend(user_id=user_id, friend_id=friend_id)
    friendship2 = Friend(user_id=friend_id, friend_id=user_id)

    db.session.add(friendship1)
    db.session.add(friendship2)
    db.session.commit()
    return {"message": f"Friend added"}, 201


@app.route('/users/<int:user_id>/friends/', methods=['GET'])
def get_friends(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404

    friend_links = Friend.query.filter_by(user_id=user_id).all()
    friends = []
    for f in friend_links:
        friend_user = User.query.get(f.friend_id)
        if friend_user:  # Only include if friend exists
            friends.append({"id": f.friend_id, "username": friend_user.username})
    return jsonify(friends)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404
    return {"id": user.id, "username": user.username}, 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return {"error": "username and password are required"}, 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return {"error": "Invalid username or password"}, 401

    return {"message": "Login successful", "user_id": user.id}, 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)