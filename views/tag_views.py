import sqlite3
import json

def create_tag(tag_data):
    with sqlite3.connect("./loaddata.sql") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Tags (label)
            VALUES (?)
            """,
            (tag_data['label'],)
        )

        conn.commit()
        return db_cursor.lastrowid
    

def get_all_tags():
    with sqlite3.connect("./loaddata.sql") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("SELECT * FROM Tags")
        tags = [dict(row) for row in db_cursor.fetchall()]
    
    return json.dumps(tags)