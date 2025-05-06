from flask import Flask, request, jsonify
from models import db, Rating, Reaction
from database import init_db
from flasgger import Swagger
import yaml
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ratings.db'
init_db(app)

MOVIE_SERVICE = "http://movie_service:5006"
USER_SERVICE = "http://user_service:5001"

# Add Swagger configuration
with open("rating_service_swagger.yml", "r") as f:
    swagger_template = yaml.safe_load(f)
swagger = Swagger(app, template=swagger_template)


def user_exists(user_id):
    """Check if user exists by calling user service.

    Returns:
        (exists: bool, status_code: int or None)
    """
    try:
        response = requests.get(f"{USER_SERVICE}/users/{user_id}")
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False, None  # None indicates request failed

def movie_exists(movie_id):
    """Check if movie exists by calling movie service.

    Returns:
        (exists: bool, status_code: int or None)
    """
    try:
        response = requests.get(f"{MOVIE_SERVICE}/movie/{movie_id}/")
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False, None  # None means request failed


@app.route('/rate/<int:user_id>/<int:movie_id>/', methods=['POST'])
def rate_movie(user_id, movie_id):
    if not user_exists(user_id):
        return {"error": f"User with ID {user_id} not found"}, 404
    if not movie_exists(movie_id):
        return {"error": f"Movie with ID {movie_id} not found"}, 404

    data = request.json
    score = data.get('score')

    if not score or not (1 <= score <= 10):
        return {"error": "Score must be between 1 and 10"}, 400

    rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if rating:
        rating.score = score
    else:
        rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
        db.session.add(rating)

    db.session.commit()
    return {"message": f"Rated movie {movie_id} with score {score}"}, 201


@app.route('/rate/<int:user_id>/<int:movie_id>/agree', methods=['POST'])
@app.route('/rate/<int:user_id>/<int:movie_id>/disagree', methods=['POST'])
def react_to_rating(user_id, movie_id):
    if not user_exists(user_id):
        return {"error": f"User with ID {user_id} not found"}, 404
    if not movie_exists(movie_id):
        return {"error": f"Movie with ID {movie_id} not found"}, 404

    data = request.json
    reactor_id = data.get('reactor_id')

    if not reactor_id:
        return {"error": "reactor_id is required"}, 400
    if not user_exists(reactor_id):
        return {"error": f"Reactor with ID {reactor_id} not found"}, 404

    # Check if the rating exists
    rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if not rating:
        return {"error": "Rating not found to react to"}, 404

    # Agree or Disagree ?
    if request.path.endswith('/agree'):
        reaction_type = 'agree'
    elif request.path.endswith('/disagree'):
        reaction_type = 'disagree'
    else:
        return {"error": "Invalid reaction endpoint"}, 400

    # One reaction per user per rating
    existing = Reaction.query.filter_by(user_id=user_id, movie_id=movie_id, reactor_id=reactor_id).first()
    if existing:
        existing.reaction_type = reaction_type
    else:
        reaction = Reaction(user_id=user_id, movie_id=movie_id, reactor_id=reactor_id, reaction_type=reaction_type)
        db.session.add(reaction)

    db.session.commit()
    return {"message": f"{reaction_type.title()}d with rating"}, 201


@app.route('/rate/<int:user_id>/', methods=['GET'])
def get_ratings(user_id):
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)