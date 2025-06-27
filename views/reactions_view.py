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
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
             """
            INSERT INTO Reactions (label, emoji, img_url)
            VALUES(?, ?, ?)
            """,
            (reaction_data['label'], reaction_data['emoji'], reaction_data['img_url'])
        )

    return json.dumps(reaction_data)

def delete_reaction(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
        """
        DELETE FROM reactions WHERE id = ?
        """, (pk,)
        )
        number_of_rows = db_cursor.rowcount

    return True if number_of_rows > 0 else False

def add_post_reaction(reaction_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
        """
        INSERT INTO PostReactions (user_id, reaction_id, post_id)
        VALUES(?, ?, ?)
        """,
        (reaction_data['user_id'], reaction_data['reaction_id'], reaction_data['post_id'])

        )
    return json.dumps(reaction_data)

def get_post_reactions(post_id=None):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        if post_id:
            db_cursor.execute("""
            SELECT
                r.id,
                r.label,
                r.emoji,
                r.img_url,
                COUNT(pr.id) as count
            FROM PostReactions pr
            JOIN Reactions r ON pr.reaction_id = r.id
            WHERE pr.post_id = ?
            GROUP BY r.id, r.label, r.emoji, r.img_url

            """, (post_id,))
        else:
            db_cursor.execute("""
            SELECT pr.id, pr.post_id, pr.reaction_id, r.label, r.img_url
            FROM PostReactions pr
            JOIN Reactions r ON pr.reaction_id = r.id
            """)

    results = [dict(row) for row in db_cursor.fetchall()]

    return json.dumps(results)


def delete_post_reaction(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
        """
        DELETE FROM PostReactions WHERE id = ?
        """, (pk,)
        )
        number_of_rows = db_cursor.rowcount

    return True if number_of_rows > 0 else False
