import sqlite3
import json
from models import Snake, Species


def get_all_snakes():
    # Open a connection to the database
    with sqlite3.connect("./snakes.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            s.id,
            s.name,
            s.owner_id,
            s.species_id,
            s.gender,
            s.color
        FROM Snakes s
        """)

        # Initialize an empty list to hold all snake representations
        snakes = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an snake instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Snake class above.
            snake = Snake(row['id'], row['name'], row['owner_id'],
                          row['species_id'], row['gender'],
                          row['color'])

            snakes.append(snake.__dict__)

    return snakes


def get_single_snake(id):
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.name,
            s.owner_id,
            s.species_id,
            s.gender,
            s.color,
			p.name species_name
        FROM Snakes s
		JOIN Species p ON p.id = s.species_id
        WHERE s.id = ?
        """, (id, ))

        # Load the single result into memory
        dataset = db_cursor.fetchall()

        snakes = []

        for row in dataset:

            snake = Snake(row['id'], row['name'], row['owner_id'],
                          row['species_id'], row['gender'],
                          row['color'])

            species = Species(row['species_id'], row['species_name'])

            snake.species = species.__dict__

            snakes.append(snake.__dict__)

            if snake.species_id == 2:
                snakes = {
                    "message": "no snake here"
                }

            else:

                return snakes


def get_snakes_by_species(species_id):

    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.owner_id,
            c.species_id,
            c.gender,
            c.color
        from Snakes c
        WHERE c.species_id = ?
        """, (species_id, ))

        snakes = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            snake = Snake(row['id'], row['name'], row['owner_id'],
                          row['species_id'], row['gender'], row['color'])
            snakes.append(snake.__dict__)

    return snakes
