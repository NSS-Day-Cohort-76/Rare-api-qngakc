import sqlite3
import json
from datetime import datetime

def getAllPosts():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                Posts.id,
                Posts.title,
                Posts.approved,
                Users.first_name || ' ' || Users.last_name AS author,
                Posts.user_id AS author_id,
                Posts.publication_date,
                Categories.label AS category,
                GROUP_CONCAT(Tags.label, ', ') AS tags
            FROM Posts
            JOIN Users ON Posts.user_id = Users.id
            JOIN Categories ON Posts.category_id = Categories.id
            LEFT JOIN PostTags ON Posts.id = PostTags.post_id
            LEFT JOIN Tags ON PostTags.tag_id = Tags.id
            GROUP BY Posts.id;
            """
        )
        query_results = db_cursor.fetchall()

        posts = []
        for row in query_results:
            posts.append(dict(row))

        serialized_posts = json.dumps(posts)

    return serialized_posts

def retrieve_myposts(pk, url):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
    SELECT 
        Posts.id AS post_id,
        Posts.title,
        Posts.approved,
        Users.first_name || ' ' || Users.last_name AS author,
        Posts.publication_date,
        Categories.label AS category,
        GROUP_CONCAT(Tags.label, ', ') AS tags
        FROM Posts
        JOIN Users ON Posts.user_id = Users.id
        JOIN Categories ON Posts.category_id = Categories.id
        LEFT JOIN PostTags ON Posts.id = PostTags.post_id
        LEFT JOIN Tags ON PostTags.tag_id = Tags.id
        WHERE Posts.user_id = ?
        GROUP BY Posts.id;
        """, (url["pk"],))

        rows = db_cursor.fetchall()
        mypost_list = []
        for row in rows:
            mypost_list.append(dict(row))

    return json.dumps(mypost_list)




def getSinglePost(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                p.id,
                p.user_id,
                p.category_id,
                c.label AS category_label,
                p.title,
                p.publication_date,
                p.image_url,
                p.content,
                p.approved,
                users.first_name,
                users.last_name
            FROM Posts p  
            JOIN Users ON p.user_id = Users.id
            LEFT JOIN Categories c ON p.category_id = c.id
            WHERE p.id = ?
            """,
            (pk,),
        )

        post_row = db_cursor.fetchone()
        if not post_row:
            return json.dumps({"error": "Post not found"})

        post = dict(post_row)

        db_cursor.execute(
            """
            SELECT t.id, t.label
            FROM Tags t
            JOIN PostTags pt ON pt.tag_id = t.id
            WHERE pt.post_id = ?
            """,
            (pk,),
        )

        tag_rows = db_cursor.fetchall()
        tags = [dict(row) for row in tag_rows]

        post["tags"] = tags
    print(json.dumps(post, indent=2))
    return json.dumps(post)


def create_post(post_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            "SELECT is_admin FROM Users WHERE id = ?",
            (post_data['author_id'],)
        )
        result = db_cursor.fetchone()
        is_admin = result[0] if result else 0

        approved = True if is_admin else False

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
                approved,
            )
        )

        post_id = db_cursor.lastrowid

        tag_ids = post_data.get("tag_ids", [])
        for tag_id in tag_ids:
            db_cursor.execute(
                """
                INSERT INTO PostTags (post_id, tag_id)
                VALUES (?, ?)
                """,
                (post_id, tag_id)
            )

        return post_id


def delete_post(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Posts WHERE id = ?
        """, (pk,)
        )
        number_of_rows = db_cursor.rowcount
    
    return True if number_of_rows > 0 else False

def update_post(pk, post_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        fields = []
        values = []

        if "title" in post_data: 
            fields.append("title = ?")
            values.append(post_data["title"])
            
        if "category_id" in post_data:
            fields.append("category_id = ?")
            values.append(post_data["category_id"])

        if "content" in post_data:
            fields.append("content = ?")
            values.append(post_data["content"])

        if "image_url" in post_data:
            fields.append("image_url = ?")
            values.append(post_data["image_url"])

        if "approved" in post_data:
            fields.append("approved = ?")
            values.append(post_data["approved"])

        values.append(pk)

        db_cursor.execute(
            f"""
            UPDATE Posts
            SET
            {', '.join(fields)}
            WHERE id = ?
            """, values
        )

        

        db_cursor.execute("DELETE FROM PostTags WHERE post_id = ?", (pk,))

        tag_ids = post_data.get("tag_ids", [])
        for tag_id in tag_ids:
            db_cursor.execute(
                "INSERT INTO PostTags (post_id, tag_id) VALUES (?, ?)",
                (pk, tag_id)
            )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False
