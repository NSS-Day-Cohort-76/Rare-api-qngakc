import sqlite3
import json
from datetime import datetime


def login_user(user):
    """Checks for the user in the database

    Args:
        user (dict): Contains the username and password of the user trying to login

    Returns:
        json string: If the user was found will return valid boolean of True and the user's id as the token
                     If the user was not found will return valid boolean False
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            select id, username, active
            from Users
            where username = ?
            and password = ?
        """,
            (user["username"], user["password"]),
        )

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None and user_from_db['active'] == 1:
            response = {
                'valid': True,
                'token': user_from_db['id']
            }
        else:
            response = {"valid": False}

        return json.dumps(response)


def create_user(user):
    """Adds a user to the database when they register

    Args:
        user (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created user
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        Insert into Users (first_name, last_name, username, email, password, bio, created_on, active) values (?, ?, ?, ?, ?, ?, ?, 1)
        """,
            (
                user["first_name"],
                user["last_name"],
                user["username"],
                user["email"],
                user["password"],
                user["bio"],
                datetime.now(),
            ),
        )

        id = db_cursor.lastrowid

        return {"token": id, "valid": True}


def get_all_users():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("SELECT * FROM Users")
        query_results = db_cursor.fetchall()

        posts = []
        for row in query_results:
            posts.append(dict(row))

        serialized_posts = json.dumps(posts)

    return serialized_posts

def get_single_user(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("SELECT * FROM Users WHERE id = ?", (pk,))

        user_row = db_cursor.fetchone()
        user= dict(user_row)

    return json.dumps(user)

def get_one_user(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
    SELECT id, first_name, last_name, admin_id, profile_image_url, bio, created_on
    FROM Users
    WHERE id = ?
""",
            (pk,),
        )

        row = db_cursor.fetchone()

        if row:
            return json.dumps(dict(row))

        else:
            return None


def create_subscription(url):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
    INSERT INTO Subscriptions (follower_id, author_id, created_on)
     VALUES (?, ?, ?)
""",
            (int(url["follower_id"]), int(url["author_id"]), url["created_on"]),
        )

        id = db_cursor.lastrowid

        return json.dumps({"token": id, "valid": True})


def get_all_subscriptions():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
    SELECT id, follower_id, author_id, created_on 
    FROM Subscriptions
"""
        )
        rows = db_cursor.fetchall()

        subscription = [dict(row) for row in rows]

        return json.dumps(subscription)


def delete_subscription(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
    DELETE FROM Subscriptions
    WHERE id = ?

    """,
            (pk,),
        )

        if db_cursor.rowcount > 0:
            return json.dumps({"deleted": True, "subscription_id": pk})
        
        else: 
            return json.dumps({"deleted": False, "subscription_id": "Not Found"})
        return json.dumps({
            'token': id,
            'valid': True
        })

def update_user_status(pk, request_body):
    new_status = request_body.get("active", 0)

    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
            UPDATE Users
            SET active = ?
            WHERE id = ?
        """, (new_status, pk))
        conn.commit()

    return db_cursor.rowcount > 0

def update_admin_status(pk, request_body):
    new_status = request_body.get("is_admin")

    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
            UPDATE Users
            SET is_admin = ?
            WHERE id = ?
        """, (new_status, pk))
        conn.commit()

    return db_cursor.rowcount > 0

