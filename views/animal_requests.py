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

animal = []

def get_all_animals():
    return ANIMALS

def get_single_animal(id):
    """Get's a single animal from the ANIMALS list

    Args:
        id (int): The requested animal id

    Returns:
        [type]: [description]
    """
    requested_animal = None
    for animal in ANIMALS:
        if animal['id'] == id:
            requested_animal = animal
    return requested_animal

def create_animal(animal):
    last_id = ANIMALS[-1]['id']
    new_id = last_id + 1

    animal['id'] = new_id
    ANIMALS.append(animal)

    return animal

def delete_animal(id):
    animal_index = -1
    for index, animal in enumerate(ANIMALS):
        if animal['id'] == id:
            animal_index = index

    if animal_index > -1:
        ANIMALS.pop(animal_index)


def update_animal(id, updated_animal):
    for index, animal in enumerate(ANIMALS):
        if animal['id'] == id:
            ANIMALS[index] = updated_animal
            break
