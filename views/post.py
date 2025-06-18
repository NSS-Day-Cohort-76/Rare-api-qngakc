import json
import sqlite3
from datetime import datetime

def list_posts():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                p.id,
                p.user_id,
                p.category_id,
                p.title,
                p.publication_date,
                p.image_url,
                p.content,
                p.approved
            FROM Posts p
        """)

        query_results = db_cursor.fetchall()
        posts = [dict(row) for row in query_results]
        return json.dumps(posts)



def create_post(post_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Posts
                (user_id, category_id, title, publication_date, image_url, content, approved)
            VALUES
                (?, ?, ?, ?, ?, ?, ?)
            """,
        (
            post_data['author_id'],
            post_data['category'],
            post_data['title'],
            datetime.now().isoformat(), 
            post_data.get('header_image_url', None),
            post_data['content'],
            True,
        )
    )
    
    return True

