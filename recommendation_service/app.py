from flask import Flask, jsonify
from flask_cors import CORS
import requests
from collections import defaultdict
from flasgger import Swagger
import yaml
import random

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # Allow frontend on localhost:3000

# Load Swagger API documentation
with open("recommendation_service_swagger.yml", "r") as f:
    swagger_template = yaml.safe_load(f)
swagger = Swagger(app, template=swagger_template)

# External service endpoints
USER_SERVICE = "http://user_service:5001"
WATCH_SERVICE = "http://watch_history_service:5002"
RATING_SERVICE = "http://rating_service:5003"

@app.route('/health', methods=['GET'])
def health_check():
    return 'OK', 200


def user_exists(user_id):
    """Check if a user exists using the User microservice."""
    try:
        response = requests.get(f"{USER_SERVICE}/users/{user_id}")
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False, None


@app.route('/recommendations/top/<int:user_id>/', methods=['GET'])
def top_rated(user_id):
    """
    GET endpoint for top 5 movies with the highest average rating from all users.

    Logic:
    - Check if the user exists.
    - Fetch ratings for users with IDs 1 through 20.
    - Aggregate scores by movie ID.
    - Compute average score per movie.
    - Return top 5 movies with the highest average score.
    """
    if not user_exists(user_id):
        return {"error": f"User with ID {user_id} not found"}, 404

    all_scores = defaultdict(list)

    for uid in range(1, 21):
        try:
            res = requests.get(f"{RATING_SERVICE}/ratings/{uid}/")
            if res.status_code == 200:
                for rating in res.json():
                    all_scores[rating["movie_id"]].append(rating["score"])
        except Exception:
            continue

    averages = []
    for mid, scores in all_scores.items():
        if scores:
            avg = sum(scores) / len(scores)
            averages.append((mid, avg))

    top = sorted(averages, key=lambda x: x[1], reverse=True)[:5]
    return jsonify([{"movie_id": mid, "avg_score": round(avg, 2)} for mid, avg in top])


@app.route('/recommendations/friends/<int:user_id>/', methods=['GET'])
def friends_unseen(user_id):
    """
    GET endpoint for recommending movies that friends have seen but the user hasn’t.

    Logic:
    - Validate user.
    - Get user’s friends from the User service.
    - Get user’s watch history.
    - Get each friend's watch history.
    - Recommend up to 5 movies seen by friends but not seen by the user.
    """
    if not user_exists(user_id):
        return {"error": f"User with ID {user_id} not found"}, 404

    # 1. Get friends list
    friends = requests.get(f"{USER_SERVICE}/users/{user_id}/friends/").json()

    # 2. Get user's own watch history
    watched = requests.get(f"{WATCH_SERVICE}/watch_history/{user_id}/").json()
    watched_ids = {w["movie_id"] for w in watched}

    # 3. Get watch history of all friends
    friend_seen = set()
    for friend in friends:
        try:
            friend_id = friend["id"]
            f_history = requests.get(f"{WATCH_SERVICE}/watch_history/{friend_id}/").json()
            friend_seen.update(w["movie_id"] for w in f_history)
        except:
            continue

    # 4. Recommend movies that friends watched but user did not
    recommendations = list(friend_seen - watched_ids)
    return jsonify({"recommendations": recommendations[:5]})


@app.route('/recommendations', methods=['GET'])
def random_recommendations():
    """
    GET endpoint to recommend 5 random movies from all rated movies (users 1–20).

    This can serve as a fallback recommendation system.
    """
    all_movies = set()

    for uid in range(1, 21):
        try:
            res = requests.get(f"{RATING_SERVICE}/ratings/{uid}/")
            if res.status_code == 200:
                for rating in res.json():
                    all_movies.add(rating["movie_id"])
        except Exception:
            continue

    selected = random.sample(list(all_movies), min(5, len(all_movies)))
    return jsonify({"recommendations": selected})


# Start the Flask server on port 5004
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
