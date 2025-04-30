from flask import Flask, jsonify
import requests
from collections import defaultdict

app = Flask(__name__)

USER_SERVICE = "http://localhost:5001"
WATCH_SERVICE = "http://localhost:5002"
RATING_SERVICE = "http://localhost:5003"

@app.route('/recommend/top/<int:user_id>/', methods=['GET'])

@app.route('/recommend/top/<int:user_id>/', methods=['GET'])
def top_rated(user_id):
    all_scores = defaultdict(list)

    # Try user IDs 1 to 20
    for uid in range(1, 21):
        try:
            res = requests.get(f"{RATING_SERVICE}/rate/{uid}/")
            if res.status_code == 200:
                for rating in res.json():
                    all_scores[rating["movie_id"]].append(rating["score"])
        except Exception as e:
            continue

    # Compute averages
    averages = []
    for mid, scores in all_scores.items():
        if scores:
            avg = sum(scores) / len(scores)
            averages.append((mid, avg))

    # Top 5 by average score
    top = sorted(averages, key=lambda x: x[1], reverse=True)[:5]
    return jsonify([{"movie_id": mid, "avg_score": round(avg, 2)} for mid, avg in top])

@app.route('/recommend/friends/<int:user_id>/', methods=['GET'])
def friends_unseen(user_id):
    # 1. Get user's friends
    friends = requests.get(f"{USER_SERVICE}/users/{user_id}/friends/").json()

    # 2. Get user's own watch history
    watched = requests.get(f"{WATCH_SERVICE}/watch/{user_id}/").json()
    watched_ids = {w["movie_id"] for w in watched}

    # 3. Collect movies watched by friends
    friend_seen = set()
    for friend in friends:
        try:
            friend_id = friend["id"]
            f_history = requests.get(f"{WATCH_SERVICE}/watch/{friend_id}/").json()
            friend_seen.update(w["movie_id"] for w in f_history)
        except:
            continue

    # 4. Recommend movies friends saw but user didn’t
    recommendations = list(friend_seen - watched_ids)
    return jsonify({"recommendations": recommendations[:5]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
