import requests
import time

BASE_URL_USER_SERVICE = "http://localhost:5001"
BASE_URL_WATCH_HISTORY_SERVICE = "http://localhost:5002"
BASE_URL_RATING_SERVICE = "http://localhost:5003"


def print_title(title):
    print(f"\n{'='*10} {title} {'='*10}")


# Create Users
print_title("Functionality 1: Create Users")
users = ['alice', 'bob', 'carol']
user_ids = {}

for name in users:
    response = requests.post(f"{BASE_URL_USER_SERVICE}/users/", json={"username": name})
    data = response.json()
    print(f"Created user '{name}':", data)
    user_ids[name] = data.get("user_id")
    time.sleep(0.3)

# Add Friends
print_title("Functionality 2: Add Friends")

# alice adds bob as a friend
response = requests.post(
    f"{BASE_URL_USER_SERVICE}/users/{user_ids['alice']}/friends/",
    json={"friend_id": user_ids['bob']}
)
print("Alice adds Bob:", response.json())
time.sleep(0.3)

# alice adds carol as a friend
response = requests.post(
    f"{BASE_URL_USER_SERVICE}/users/{user_ids['alice']}/friends/",
    json={"friend_id": user_ids['carol']},
)
print("Alice adds Carol:", response.json())
time.sleep(0.3)

# Get Alice's Friends
print_title("List Friends of Alice")
response = requests.get(f"{BASE_URL_USER_SERVICE}/users/{user_ids['alice']}/friends/")
print("Alice's friends:", response.json())
time.sleep(0.3)

# Add Movies to Watch History
print_title("Functionality 3: Add Movies to Watch History")

# User alice watches movie with ID 101
response = requests.post(
    f"{BASE_URL_WATCH_HISTORY_SERVICE}/watch/{user_ids['alice']}/101/",
)
print("Alice watches movie 101:", response.json())
time.sleep(0.3)

# User bob watches movie with ID 102
response = requests.post(
    f"{BASE_URL_WATCH_HISTORY_SERVICE}/watch/{user_ids['bob']}/102/",
)
print("Bob watches movie 102:", response.json())
time.sleep(0.3)

# User carol watches movie with ID 103
response = requests.post(
    f"{BASE_URL_WATCH_HISTORY_SERVICE}/watch/{user_ids['carol']}/103/",
)
print("Carol watches movie 103:", response.json())
time.sleep(0.3)

# Get Watch History for Users
print_title("Get Watch History for Users")

# Get Alice's watch history
response = requests.get(f"{BASE_URL_WATCH_HISTORY_SERVICE}/watch/{user_ids['alice']}/")
print("Alice's watch history:", response.json())
time.sleep(0.3)

# Get Bob's watch history
response = requests.get(f"{BASE_URL_WATCH_HISTORY_SERVICE}/watch/{user_ids['bob']}/")
print("Bob's watch history:", response.json())
time.sleep(0.3)

# Get Carol's watch history
response = requests.get(f"{BASE_URL_WATCH_HISTORY_SERVICE}/watch/{user_ids['carol']}/")
print("Carol's watch history:", response.json())
time.sleep(0.3)

# Rate Movies
print_title("Functionality 4: Rate Movies")

response = requests.post(
    f"{BASE_URL_RATING_SERVICE}/rate/{user_ids['alice']}/101/",
    json={"score": 9}
)
print("Alice rates movie 101 with score 9:", response.json())
time.sleep(0.3)

response = requests.post(
    f"{BASE_URL_RATING_SERVICE}/rate/{user_ids['bob']}/102/",
    json={"score": 8}
)
print("Bob rates movie 102 with score 8:", response.json())
time.sleep(0.3)

# Agree/Disagree with Ratings
print_title("Functionality 5: React to Ratings")

response = requests.post(
    f"{BASE_URL_RATING_SERVICE}/rate/{user_ids['alice']}/101/agree",
    json={"reactor_id": user_ids['bob']}
)
print("Bob agrees with Alice's rating on movie 101:", response.json())
time.sleep(0.3)

response = requests.post(
    f"{BASE_URL_RATING_SERVICE}/rate/{user_ids['bob']}/102/disagree",
    json={"reactor_id": user_ids['carol']}
)
print("Carol disagrees with Bob's rating on movie 102:", response.json())
time.sleep(0.3)

# Get Ratings with Reactions
print_title("Functionality 6: Get Ratings for Users")

response = requests.get(f"{BASE_URL_RATING_SERVICE}/rate/{user_ids['alice']}/")
print("Alice's ratings:", response.json())
time.sleep(0.3)

response = requests.get(f"{BASE_URL_RATING_SERVICE}/rate/{user_ids['bob']}/")
print("Bob's ratings:", response.json())
time.sleep(0.3)
