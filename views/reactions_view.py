import sqlite3
import json

def get_all_reactions():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("SELECT * FROM Reactions")
        reactions = [dict(row) for row in db_cursor.fetchall()]

    return json.dumps(reactions)
