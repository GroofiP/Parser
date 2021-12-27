import json

import requests

username = "GroofiP"

url = f"https://api.github.com/users/{username}/repos"
responce = requests.get(url)
data = responce.json()
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)
