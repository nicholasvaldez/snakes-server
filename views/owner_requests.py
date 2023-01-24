import sqlite3
import json
from models import Owner


def get_all_owners():
    # Open a connection to the database
    with sqlite3.connect("./snakes.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            o.id,
            o.first_name,
            o.last_name,
            o.email
        FROM Owners o
        """)

        owners = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            owner = Owner(row['id'], row['first_name'], row['last_name'],
                          row['email'])

            owners.append(owner.__dict__)

    return owners


def get_single_owner(id):
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            o.id,
            o.first_name,
            o.last_name,
            o.email
        FROM Owners o
        WHERE o.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        owner = Owner(data['id'], data['first_name'], data['last_name'],
                      data['email'])

        return owner.__dict__
