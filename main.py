import requests
import json
import os

game_id = '/nfl/boxscore/_/gameId/401872995'
url = f"http://espn.com{game_id}"
headers = {"User-Agent": "Mozilla/5.0"}
data = ''


response = requests.get(url, headers=headers)
response.raise_for_status()

with open("FootballDB/test.html", "w") as f:
    f.write(response.text)

# response = requests.get(url, headers=headers)
# response.raise_for_status()
# if (response.status_code == 200):
#     data = response.json()

# filename = 'test.json'
# with open(filename, 'w') as f:
#     json.dump(data, f)