import sqlite3
import json
from models import Species


def get_all_species():
    # Open a connection to the database
    with sqlite3.connect("./snakes.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            s.id,
            s.name
        FROM Species s
        """)

        # Initialize an empty list to hold all snake representations
        speciess = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            species = Species(row['id'], row['name'])

            speciess.append(species.__dict__)

    return speciess
