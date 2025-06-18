import sqlite3
import json

def retrieve_posts(url): 
  with sqlite3.connect("./db.sqlite3") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    post_list = []

    if url["requested_resource"] == "post":
      db_cursor.execute("""
    SELECT 
  post.id,
  post.category_id,
  post.title,
  post.publication_date,
  post.image_url,
  post.content
    FROM Posts as post
    """)
    query_results = db_cursor.fetchall()
    for row in query_results:
      post_list.append(dict(row))

  return json.dumps(post_list)