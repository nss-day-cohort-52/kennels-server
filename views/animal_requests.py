import sqlite3
import json
from models import Animal
ANIMALS = [
    {
        "id": 1,
        "name": "Snickers",
        "species": "Dog",
        "locationId": 1,
        "customerId": 4
    },
    {
        "id": 2,
        "name": "Gypsy",
        "species": "Dog",
        "locationId": 1,
        "customerId": 2
    },
    {
        "id": 3,
        "name": "Blue",
        "species": "Cat",
        "locationId": 2,
        "customerId": 1
    }
]


def get_all_animals():
    """Return the ANIMALS list"""
    with sqlite3.connect('./kennel.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            select a.id,
                a.name,
                a.breed,
                a.status,
                a.location_id,
                a.customer_id
            from animal a
        """)

        dataset = db_cursor.fetchall()

        animals = []

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'], row['status'], row['location_id'], row['customer_id'])

            animals.append(animal.__dict__)

        return json.dumps(animals)



def get_single_animal(id):
    """Get's a single animal from the Animal table

    Args:
        id (int): The requested animal id

    Returns:
        dictionary: the requested animal
    """
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(data['id'], data['name'], data['breed'],
                            data['status'], data['location_id'],
                            data['customer_id'])

        return json.dumps(animal.__dict__)


def create_animal(animal):
    """Add the animal to the ANIMALS list

    Args:
        animal (dict): the new animal

    Returns:
        dictionary: the new animal
    """
    last_id = ANIMALS[-1]['id']
    new_id = last_id + 1

    animal['id'] = new_id
    ANIMALS.append(animal)

    return animal


def delete_animal(id):
    """Remove an animal from the list

    Args:
        id (int): the id of the animal to remove
    """
    animal_index = -1
    for index, animal in enumerate(ANIMALS):
        if animal['id'] == id:
            animal_index = index

    if animal_index > -1:
        ANIMALS.pop(animal_index)


def update_animal(id, updated_animal):
    """Update an animal in the list

    Args:
        id (int): the id of the animal to update
        updated_animal (dict): the updated animal dictionary
    """
    for index, animal in enumerate(ANIMALS):
        if animal['id'] == id:
            ANIMALS[index] = updated_animal
            break
