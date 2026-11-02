import sqlite3

connection = sqlite3.connect("football.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        name TEXT PRIMARY KEY,
        age INTEGER,
        position TEXT,
        team TEXT
    )
""")

cursor.execute(
    "INSERT INTO players (name, age, position, team) VALUES (?, ?, ?, ?)",
    ("puka nacua", 25, "wr", "LA RAMS")
)

connection.commit()

cursor.execute("SELECT * FROM players WHERE name = ?", ("puka nacua",))
puka = cursor.fetchone()

print(puka)