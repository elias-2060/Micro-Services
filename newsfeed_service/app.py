from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

USER_SERVICE = "http://user_service:5001"
WATCH_SERVICE = "http://watch_history_service:5002"


@app.route('/newsfeed/<int:user_id>/', methods=['GET'])
def get_newsfeed(user_id):
    try:
        # 1. Get user's friends
        friends_response = requests.get(f"{USER_SERVICE}/users/{user_id}/friends/")
        if friends_response.status_code != 200:
            return jsonify({"error": "Failed to fetch friends"}), 500

        friends = friends_response.json()
        if not friends:
            return jsonify({"message": "No friends found", "newsfeed": []})

        # 2. Get watch history for each friend
        newsfeed_items = []
        for friend in friends:
            friend_id = friend["id"]
            try:
                history_response = requests.get(f"{WATCH_SERVICE}/watch/{friend_id}/")
                if history_response.status_code == 200:
                    friend_history = history_response.json()
                    # Only include recent watches (last 7 days)
                    recent_watches = [
                        item for item in friend_history
                        if datetime.fromisoformat(item["timestamp"]) > datetime.utcnow() - timedelta(days=7)
                    ]
                    for watch in recent_watches:
                        newsfeed_items.append({
                            "friend_id": friend_id,
                            "friend_username": friend["username"],
                            "movie_id": watch["movie_id"],
                            "timestamp": watch["timestamp"]
                        })
            except requests.exceptions.RequestException:
                continue

        # 3. Sort by timestamp (newest first)
        newsfeed_items.sort(key=lambda x: x["timestamp"], reverse=True)

        # 4. Limit to 20 most recent items
        return jsonify({"newsfeed": newsfeed_items[:20]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
