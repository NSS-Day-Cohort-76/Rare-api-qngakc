import sqlite3
import json

def display_comments(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
      conn.row_factory = sqlite3.Row
      db_cursor = conn.cursor()
# passing in the postId so that we can only fetch the comments with post_id = postId
      comments_list = []
      db_cursor.execute("""
  SELECT 
  Comments.author_id,
  Comments.post_id,
  Comments.content,
  Users.first_name,
  Users.last_name       
  FROM Comments
  JOIN Users ON Users.id == Comments.author_id
  WHERE Comments.post_id = ?
""", (pk,))
      query_results = db_cursor.fetchall()
      for row in query_results: 
         comments_list.append(dict(row))

      return json.dumps(comments_list)
    

def create_comment(url):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            INSERT INTO Comments
            (author_id, post_id, content)
            VALUES (?, ?, ?)
        """, (url["author_id"], url["post_id"], url["content"]))

        return {
            "message": "Comment created successfully",
            "author_id": url["author_id"],
            "post_id": url["post_id"],
            "content": url["content"]
        }
