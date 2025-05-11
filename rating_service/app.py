from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Rating, Reaction
from database import init_db
from flasgger import Swagger
import yaml
import requests

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # Allow frontend on localhost:3000
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ratings.db'  # SQLite database for local ratings storage
init_db(app)  # Initialize the database with tables

# External service endpoints
MOVIE_SERVICE = "http://movie_service:5006"
USER_SERVICE = "http://user_service:5001"

# Load Swagger documentation config
with open("rating_service_swagger.yml", "r") as f:
    swagger_template = yaml.safe_load(f)
swagger = Swagger(app, template=swagger_template)

def user_exists(user_id):
    """Check if a user exists using the User microservice."""
    try:
        response = requests.get(f"{USER_SERVICE}/users/{user_id}")
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False, None

def movie_exists(movie_id):
    """Check if a movie exists using the Movie microservice."""
    try:
        response = requests.get(f"{MOVIE_SERVICE}/movie/{movie_id}/")
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False, None

@app.route('/ratings/<int:user_id>/<int:movie_id>/', methods=['POST'])
def rate_movie(user_id, movie_id):
    """
    POST endpoint for a user to rate a movie.

    Validates:
    - User and movie existence
    - Score must be between 1 and 10

    Behavior:
    - If rating already exists, it updates the score.
    - Otherwise, it creates a new rating.
    """
    if not user_exists(user_id):
        return {"error": f"User with ID {user_id} not found"}, 404
    if not movie_exists(movie_id):
        return {"error": f"Movie with ID {movie_id} not found"}, 404

    data = request.json
    score = data.get('score')

    if not score or not (1 <= score <= 10):
        return {"error": "Score must be between 1 and 10"}, 400

    # Upsert logic: update if exists, else insert
    rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if rating:
        rating.score = score
    else:
        rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
        db.session.add(rating)

    db.session.commit()
    return {"message": f"Rated movie {movie_id} with score {score}"}, 201

@app.route('/ratings/<int:user_id>/<int:movie_id>/reaction', methods=['POST'])
def react_to_rating(user_id, movie_id):
    """
    POST endpoint to react (agree/disagree) to a user's movie rating.

    Validates:
    - User, movie, and reactor existence
    - Valid reaction type (agree/disagree)

    Behavior:
    - Adds or updates a reaction record by the reactor to the specified rating.
    """
    if not user_exists(user_id):
        return {"error": f"User with ID {user_id} not found"}, 404
    if not movie_exists(movie_id):
        return {"error": f"Movie with ID {movie_id} not found"}, 404

    data = request.json
    reactor_id = data.get('reactor_id')
    reaction_type = data.get('reaction_type')

    if not reactor_id:
        return {"error": "reactor_id is required"}, 400
    if not reaction_type:
        return {"error": "'reaction-type' is required "}, 400
    if reaction_type not in ['agree', 'disagree']:
        return {"error": "Invalid reaction_type. Must be 'agree' or 'disagree'"}, 400
    if not user_exists(reactor_id):
        return {"error": f"Reactor with ID {reactor_id} not found"}, 404

    rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if not rating:
        return {"error": "Rating not found to react to"}, 404

    # Upsert logic for reactions
    existing = Reaction.query.filter_by(user_id=user_id, movie_id=movie_id, reactor_id=reactor_id).first()
    if existing:
        existing.reaction_type = reaction_type
    else:
        reaction = Reaction(
            user_id=user_id,
            movie_id=movie_id,
            reactor_id=reactor_id,
            reaction_type=reaction_type
        )
        db.session.add(reaction)

    db.session.commit()
    return {"message": f"{reaction_type.title()}d with rating"}, 201

@app.route('/ratings/<int:user_id>/', methods=['GET'])
def get_ratings(user_id):
    """
    GET endpoint to retrieve all movie ratings for a specific user.

    Returns:
    - List of ratings with movie_id, score, and counts of agree/disagree reactions.
    """
    if not user_exists(user_id):
        return {"error": f"User with ID {user_id} not found"}, 404

    ratings = Rating.query.filter_by(user_id=user_id).all()
    result = []
    for r in ratings:
        agrees = Reaction.query.filter_by(user_id=user_id, movie_id=r.movie_id, reaction_type='agree').count()
        disagrees = Reaction.query.filter_by(user_id=user_id, movie_id=r.movie_id, reaction_type='disagree').count()
        result.append({
            "movie_id": r.movie_id,
            "score": r.score,
            "agrees": agrees,
            "disagrees": disagrees
        })
    return jsonify(result)

@app.route('/reactions/<int:reactor_id>', methods=['GET'])
def get_user_reactions(reactor_id):
    """
    GET endpoint to retrieve all reactions made by a specific user (reactor).

    Returns:
    - List of reactions with user_id, movie_id, and reaction_type.
    """
    if not user_exists(reactor_id):
        return {"error": f"User with ID {reactor_id} not found"}, 404

    reactions = Reaction.query.filter_by(reactor_id=reactor_id).all()
    result = [
        {
            "user_id": r.user_id,
            "movie_id": r.movie_id,
            "reaction_type": r.reaction_type
        }
        for r in reactions
    ]
    return jsonify(result)

# Start the Flask server on port 5003
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
