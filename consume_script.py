import requests
import time

BASE_URL = "http://localhost:5001"


def print_title(title):
    print(f"\n{'='*10} {title} {'='*10}")


# 1. Create Users
print_title("Functionality 1: Create Users")
users = ['alice', 'bob', 'carol']
user_ids = {}

for name in users:
    response = requests.post(f"{BASE_URL}/users/", json={"username": name})
    data = response.json()
    print(f"Created user '{name}':", data)
    user_ids[name] = data.get("user_id")
    time.sleep(0.5)

# 2. Add Friends
print_title("Functionality 2: Add Friends")

# alice adds bob as a friend
response = requests.post(
    f"{BASE_URL}/users/{user_ids['alice']}/friends/",
    json={"friend_id": user_ids['bob']}
)
print("Alice adds Bob:", response.json())
time.sleep(0.5)

# alice adds carol as a friend
response = requests.post(
    f"{BASE_URL}/users/{user_ids['alice']}/friends/",
    json={"friend_id": user_ids['carol']}
)
print("Alice adds Carol:", response.json())
time.sleep(0.5)

# 3. Get Alice's Friends
print_title("Functionality 3: List Friends of Alice")
response = requests.get(f"{BASE_URL}/users/{user_ids['alice']}/friends/")
print("Alice's friends:", response.json())