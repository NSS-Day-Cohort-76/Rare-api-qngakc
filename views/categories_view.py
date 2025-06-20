import sqlite3
import json

def create_category(category_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Categories (label)
            VALUES (?)
            """,
            (category_data['label'],)
        )

        conn.commit()
        id = db_cursor.lastrowid
        return json.dumps({ "id": id, "label": category_data['label'] }) 
    

def get_all_categories():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("SELECT * FROM Categories")
        tags = [dict(row) for row in db_cursor.fetchall()]
    
    return json.dumps(tags)

def delete_category(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """ 
                    DELETE FROM Categories 
                    WHERE id = ? 
                """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False