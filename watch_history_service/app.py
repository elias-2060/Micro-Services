from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, WatchHistory
from database import init_db
from datetime import datetime
from flasgger import Swagger
import yaml
import requests


app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watchhistory.db'
init_db(app)

MOVIE_SERVICE = "http://movie_service:5006"
USER_SERVICE = "http://user_service:5001"

# Swagger configuration
with open("watch_service_swagger.yml", "r") as f:
    swagger_template = yaml.safe_load(f)
swagger = Swagger(app, template=swagger_template)

@app.route('/health', methods=['GET'])
def health_check():
    return 'OK', 200


def user_exists(user_id):
    """Check if user exists by calling user service"""
    try:
        response = requests.get(f"{USER_SERVICE}/users/{user_id}")
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False, None


def movie_exists(movie_id):
    """Check if movie exists by calling movie service"""
    try:
        response = requests.get(f"{MOVIE_SERVICE}/movie/{movie_id}/")
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False, None



@app.route('/watch_history/<int:user_id>/<int:movie_id>/', methods=['POST'])
def add_watch(user_id, movie_id):
    """Add a movie to a user's watch history"""
    if not user_exists(user_id):
        return {"error": f"User with ID {user_id} not found"}, 404
    if not movie_exists(movie_id):
        return {"error": f"Movie with ID {movie_id} not found"}, 404

    watch = WatchHistory(user_id=user_id, movie_id=movie_id, timestamp=datetime.utcnow())
    db.session.add(watch)
    db.session.commit()

    return {"message": f"Movie {movie_id} added to user {user_id}'s history"}, 201


@app.route('/watch_history/<int:user_id>/', methods=['GET'])
def get_watch_history(user_id):
    """Get the full watch history for a user"""
    if not user_exists(user_id):
        return {"error": f"User with ID {user_id} not found"}, 404

    history = WatchHistory.query.filter_by(user_id=user_id).all()
    output = [
        {"movie_id": entry.movie_id, "timestamp": entry.timestamp.isoformat()}
        for entry in history
    ]

    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
