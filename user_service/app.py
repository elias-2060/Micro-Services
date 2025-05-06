from flask import Flask, request, jsonify
from models import db, User, Friend
from database import init_db
from flasgger import Swagger
import yaml

app = Flask(__name__)
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
    if not username:
        return {"error": "username is required"}, 400

    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return {"message": "User created", "user_id": user.id}, 201

@app.route('/users/<int:user_id>/friends/', methods=['POST'])
def add_friend(user_id):
    data = request.json
    friend_id = data.get('friend_id')

    if not User.query.get(user_id) or not User.query.get(friend_id):
        return {"error": "User or friend not found"}, 404

    existing = Friend.query.filter_by(user_id=user_id, friend_id=friend_id).first()
    if existing:
        return {"message": "Already friends"}, 200

    friendship = Friend(user_id=user_id, friend_id=friend_id)
    db.session.add(friendship)
    db.session.commit()
    return {"message": f"Friend added"}, 201

@app.route('/users/<int:user_id>/friends/', methods=['GET'])
def get_friends(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404

    friend_links = Friend.query.filter_by(user_id=user_id).all()
    friends = [{"id": f.friend_id, "username": User.query.get(f.friend_id).username} for f in friend_links]
    return jsonify(friends)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
