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
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            users.first_name,
            users.last_name
        FROM Posts p  
        JOIN Users ON p.user_id = Users.id       
        WHERE p.id = ?
        """,
            (pk,),
        )

        query_results = db_cursor.fetchone()

    return json.dumps(dict(query_results))

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

        post_id = db_cursor.lastrowid 
        return post_id 
