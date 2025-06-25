import sqlite3
import json

def get_all_reactions():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("SELECT * FROM Reactions")
        reactions = [dict(row) for row in db_cursor.fetchall()]

    return json.dumps(reactions)

def create_reaction(reaction_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Reactions (label)
            VALUES(?)
            """,
            (reaction_data['label'], reaction_data['image_url'])
        )
        reactions = [dict(row) for row in db_cursor.fetchall()]

    return json.dumps(reactions)