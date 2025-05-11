import requests

BASE_URL_USER_SERVICE = "http://localhost:5001"
BASE_URL_WATCH_HISTORY_SERVICE = "http://localhost:5002"
BASE_URL_RATING_SERVICE = "http://localhost:5003"
BASE_URL_RECOMMENDATION_SERVICE = "http://localhost:5004"
BASE_URL_NEWSFEED_SERVICE = "http://localhost:5005"
BASE_URL_MOVIE_SERVICE = "http://localhost:5006"


def print_title(title):
    print(f"\n{'='*10} {title} {'='*10}")


# Create Friends
print_title("Functionality 1: Create Friends")
users = {
    'alice': 'password123',
    'bob': 'secure456',
    'carol': 'pass789'
}
user_ids = {}

for name, password in users.items():
    # Create user
    response = requests.post(f"{BASE_URL_USER_SERVICE}/users/", json={
        "username": name,
        "password": password
    })
    data = response.json()
    print(f"Created user '{name}':", data)

    user_id = data.get("user_id")
    if user_id:
        user_ids[name] = user_id
    else:
        # If user exists already or error, attempt to log in
        print(f"Trying login for existing user '{name}'...")
        login_resp = requests.post(f"{BASE_URL_USER_SERVICE}/login", json={
            "username": name,
            "password": password
        })
        login_data = login_resp.json()
        print(f"Login response: {login_data}")
        if login_resp.status_code == 200:
            user_ids[name] = login_data["user_id"]


# Add Friends
print_title("Functionality 2: Add Friends")

# alice adds bob as a friend
response = requests.post(
    f"{BASE_URL_USER_SERVICE}/users/{user_ids['alice']}/friends/",
    json={"friend_id": user_ids['bob']}
)
print("Alice adds Bob:", response.json())

# alice adds carol as a friend
response = requests.post(
    f"{BASE_URL_USER_SERVICE}/users/{user_ids['alice']}/friends/",
    json={"friend_id": user_ids['carol']},
)
print("Alice adds Carol:", response.json())

# Get Alice's Friends
print_title("List Friends of Alice")
response = requests.get(f"{BASE_URL_USER_SERVICE}/users/{user_ids['alice']}/friends/")
print("Alice's friends:", response.json())

# Add Movies to Watch History
print_title("Functionality 3: Add Movies to Watch History")

# User alice watches movie with ID 101
response = requests.post(
    f"{BASE_URL_WATCH_HISTORY_SERVICE}/watch_history/{user_ids['alice']}/101/",
)
print("Alice watches movie 101:", response.json())

# User bob watches movie with ID 102
response = requests.post(
    f"{BASE_URL_WATCH_HISTORY_SERVICE}/watch_history/{user_ids['bob']}/101/",
)
print("Bob watches movie 101:", response.json())

# User bob watches movie with ID 102
response = requests.post(
    f"{BASE_URL_WATCH_HISTORY_SERVICE}/watch_history/{user_ids['bob']}/102/",
)
print("Bob watches movie 102:", response.json())

# User carol watches movie with ID 103
response = requests.post(
    f"{BASE_URL_WATCH_HISTORY_SERVICE}/watch_history/{user_ids['carol']}/103/",
)
print("Carol watches movie 103:", response.json())

# User carol watches movie with ID 103
response = requests.post(
    f"{BASE_URL_WATCH_HISTORY_SERVICE}/watch_history/{user_ids['carol']}/104/",
)
print("Carol watches movie 104:", response.json())

# Get Watch History for Friends
print_title("Get Watch History for Friends")

# Get Alice's watch history
response = requests.get(f"{BASE_URL_WATCH_HISTORY_SERVICE}/watch_history/{user_ids['alice']}/")
print("Alice's watch history:", response.json())

# Get Bob's watch history
response = requests.get(f"{BASE_URL_WATCH_HISTORY_SERVICE}/watch_history/{user_ids['bob']}/")
print("Bob's watch history:", response.json())

# Get Carol's watch history
response = requests.get(f"{BASE_URL_WATCH_HISTORY_SERVICE}/watch_history/{user_ids['carol']}/")
print("Carol's watch history:", response.json())

# Rate Movies
print_title("Functionality 4: Rate Movies")

response = requests.post(
    f"{BASE_URL_RATING_SERVICE}/ratings/{user_ids['alice']}/101/",
    json={"score": 9}
)
print("Alice rates movie 101 with score 9:", response.json())

response = requests.post(
    f"{BASE_URL_RATING_SERVICE}/ratings/{user_ids['bob']}/101/",
    json={"score": 7}
)
print("Bob rates movie 101 with score 7:", response.json())

response = requests.post(
    f"{BASE_URL_RATING_SERVICE}/ratings/{user_ids['bob']}/102/",
    json={"score": 8}
)
print("Bob rates movie 102 with score 8:", response.json())

response = requests.post(
    f"{BASE_URL_RATING_SERVICE}/ratings/{user_ids['carol']}/103/",
    json={"score": 9}
)
print("Carol rates movie 103 with score 9:", response.json())

response = requests.post(
    f"{BASE_URL_RATING_SERVICE}/ratings/{user_ids['carol']}/104/",
    json={"score": 6}
)
print("Carol rates movie 104 with score 6:", response.json())



# Agree/Disagree with Ratings
print_title("Functionality 5: React to Ratings")

response = requests.post(
    f"{BASE_URL_RATING_SERVICE}/ratings/{user_ids['alice']}/101/reaction",
    json={"reactor_id": user_ids['bob'], "reaction_type": "agree"}
)
print("Bob agrees with Alice's rating on movie 101:", response.json())

response = requests.post(
    f"{BASE_URL_RATING_SERVICE}/ratings/{user_ids['bob']}/102/reaction",
    json={"reactor_id": user_ids['carol'], "reaction_type": "disagree"}
)
print("Carol disagrees with Bob's rating on movie 102:", response.json())

# Get Ratings with Reactions
print_title("Functionality 6: Get Ratings for Friends")

response = requests.get(f"{BASE_URL_RATING_SERVICE}/ratings/{user_ids['alice']}/")
print("Alice's ratings:", response.json())

response = requests.get(f"{BASE_URL_RATING_SERVICE}/ratings/{user_ids['bob']}/")
print("Bob's ratings:", response.json())

# Top-rated Movie Recommendations
print_title("Functionality 7: Top-Rated Movie Recommendations")
response = requests.get(f"{BASE_URL_RECOMMENDATION_SERVICE}/recommendations/top/{user_ids['alice']}/")
print("Top recommendations for Alice:", response.json())

# Friends watched movie Recommendations
print_title("Functionality 8: Friends-Based Movie Recommendations")
response = requests.get(f"{BASE_URL_RECOMMENDATION_SERVICE}/recommendations/friends/{user_ids['alice']}/")
print("Friend-based recommendations for Alice:", response.json())

# Newsfeed: Latest movies watched by friends
print_title("Functionality 9: Newsfeed - Latest Movies Watched by Friends")

response = requests.get(f"{BASE_URL_NEWSFEED_SERVICE}/newsfeed/{user_ids['alice']}/")
print("Newsfeed for Alice:", response.json())

# Movie Service Functionality
print_title("Functionality 10: Get Movie Information")

# Get single movie by ID
print("\nGet movie with ID 76:")
response = requests.get(f"{BASE_URL_MOVIE_SERVICE}/movie/76/")
print(response.json())

# Get list of movies
print("\nGet first 5 movies:")
response = requests.get(f"{BASE_URL_MOVIE_SERVICE}/movies/?start=0&count=5")
print(response.json())