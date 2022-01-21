import sqlite3
import json
from models.animals import Animal
from models.customers import Customer
from models.locations import Location
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
                a.customer_id,
                l.name location_name,
                l.address location_address,
                c.name customer_name,
                c.email,
                c.address customer_address
            from animal a
            join location l on l.id = a.location_id
            join customer c on c.id = a.customer_id
        """)

        dataset = db_cursor.fetchall()

        animals = []

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'], row['customer_id'])
            animal.customer = Customer(
                row['customer_id'], row['customer_name'], row['customer_address'], row['email']).__dict__
            animal.location = Location(
                row['location_id'], row['location_name'], row['location_address']).__dict__
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
            a.customer_id,
            l.name location_name,
            l.address location_address,
            c.name customer_name,
            c.email,
            c.address customer_address
        FROM animal a
        join location l on l.id = a.location_id
        join customer c on c.id = a.customer_id
        WHERE a.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(data['id'], data['name'], data['breed'],
                        data['status'], data['location_id'],
                        data['customer_id'])
        animal.customer = Customer(data['customer_id'],
                                   data['customer_name'],
                                   data['customer_address'],
                                   data['email']).__dict__
        animal.location = Location(
            data['location_id'], data['location_name'], data['location_address']).__dict__

        return json.dumps(animal.__dict__)


def create_animal(animal):
    """Add the animal to the ANIMALS list

    Args:
        animal (dict): the new animal

    Returns:
        dictionary: the new animal
    """
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            insert into Animal (name, breed, status, location_id, customer_id)
            values (?, ?, ?, ?, ?);
        """, (animal['name'], animal['breed'], animal['status'], animal['location_id'], animal['customer_id']))

        id = db_cursor.lastrowid

        animal['id'] = id

        return json.dumps(animal)



def delete_animal(id):
    """Remove an animal from the list

    Args:
        id (int): the id of the animal to remove
    """
    with sqlite3.connect('./kennel.sqlite3') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
            Delete from animal
            where id = ?
        """, (id,))

        was_updated = db_cursor.rowcount

        if was_updated == 0:
            return False
        else:
            return True


def update_animal(id, updated_animal):
    """Update an animal in the list

    Args:
        id (int): the id of the animal to update
        updated_animal (dict): the updated animal dictionary
    """
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            Update Animal
            Set 
                name = ?,
                status = ?,
                breed = ?,
                customer_id = ?,
                location_id = ?
            Where id = ?
        """, (updated_animal['name'],
              updated_animal['status'], updated_animal['breed'], updated_animal['customer_id'], updated_animal['location_id'], id))

        was_updated = db_cursor.rowcount

        if was_updated == 0:
            return False
        else:
            return True


def get_animals_by_search(text):
    animals = json.loads(get_all_animals())
    animals = [animal for animal in animals if text.lower()
               in animal['name'].lower()]
    return json.dumps(animals)
