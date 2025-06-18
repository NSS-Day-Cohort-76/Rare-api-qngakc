import sqlite3
import json

def display_comments():
    with sqlite3.connect("./db.sqlite3") as conn:
      conn.row_factory = sqlite3.Row
      db_cursor = conn.cursor()

      