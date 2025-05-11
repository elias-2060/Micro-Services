from flask import Flask, jsonify
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
from flasgger import Swagger
import yaml

# Initialize Flask application
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # Allow frontend on localhost:3000 to access this API

# Load Swagger configuration for API documentation
with open("newsfeed_service_swagger.yml", "r") as f:
    swagger_template = yaml.safe_load(f)
swagger = Swagger(app, template=swagger_template)

# URLs for the user and watch history microservices
USER_SERVICE = "http://user_service:5001"
WATCH_SERVICE = "http://watch_history_service:5002"

def user_exists(user_id):
    """
    Check if a user exists by calling the User microservice.

    Args:
        user_id (int): ID of the user to check.

    Returns:
        (bool, int or None): Tuple of whether the user exists and optional status code.
    """
    try:
        response = requests.get(f"{USER_SERVICE}/users/{user_id}")
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False, None  # Request failure

@app.route('/newsfeed/<int:user_id>/', methods=['GET'])
def get_newsfeed(user_id):
    """
    GET endpoint to retrieve a user's newsfeed based on their friends' watch activity.

    Steps:
    1. Validate that the user exists.
    2. Fetch the user's friends from the User service.
    3. For each friend, fetch their watch history from the Watch service.
    4. Filter for movies watched in the last 7 days.
    5. Return the 20 most recent watched movies sorted by timestamp.

    Returns:
        JSON response with a list of recent friend activity or error message.
    """
    try:
        # Step 1: Check if user exists
        if not user_exists(user_id):
            return {"error": f"User with ID {user_id} not found"}, 404

        # Step 2: Get user's friends from the User service
        friends_response = requests.get(f"{USER_SERVICE}/users/{user_id}/friends/")
        if friends_response.status_code != 200:
            return jsonify({"error": "Failed to fetch friends"}), 500

        friends = friends_response.json()
        if not friends:
            return jsonify({"message": "No friends found", "newsfeed": []})

        # Step 3: Fetch and filter watch history for each friend
        newsfeed_items = []
        for friend in friends:
            friend_id = friend["id"]
            try:
                history_response = requests.get(f"{WATCH_SERVICE}/watch_history/{friend_id}/")
                if history_response.status_code == 200:
                    friend_history = history_response.json()
                    # Step 4: Filter for watches within the last 7 days
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
                # Ignore failed requests for individual friends
                continue

        # Step 5: Sort newsfeed by timestamp (newest first)
        newsfeed_items.sort(key=lambda x: x["timestamp"], reverse=True)

        # Step 6: Return up to 20 most recent items
        return jsonify({"newsfeed": newsfeed_items[:20]})

    except Exception as e:
        # Catch any unexpected errors
        return jsonify({"error": str(e)}), 500

# Run the Flask app on port 5005 with debug mode enabled
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
