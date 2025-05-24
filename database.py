import sqlite3

con = sqlite3.connect("images.db")
cur = con.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS images (
        hash INTEGER PRIMARY KEY,
        tag_string_general TEXT,
        tag_string_character TEXT,
        tag_string_copyright TEXT,
        tag_string_artist TEXT,
        tag_string_meta TEXT
    )
""")
