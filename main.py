import requests, json, os, re, sqlite3
from bs4 import BeautifulSoup

# for loop so that we can record everygame in a season into the db fast
#should have a game db, aswell as a individual player db
# a way to find the id for every nfl game that season?
year = 2026
schedule_url = f"https://www.espn.com/nfl/schedulegrid/_/year/{year}"
scheduleHtml = requests.get(schedule_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text

# with open(f"schedule{year}.html", "w") as f:
#     f.write(scheduleHtml)

with open("schedule2026.html", encoding="iso-8859-1") as f:
    soup = BeautifulSoup(f, "html.parser")
table = soup.find("table", class_="tablehead")
with open("schedule_table.html", "w", encoding="utf-8") as out:
    out.write(str(table))

