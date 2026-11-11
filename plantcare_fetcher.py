import json
import requests
from datetime import datetime
import pickle


def get_idex() -> dict:
    """ Get file containing all slugs of every plant """
    response = requests.get("https://www.plantsolve.com/api/v1/plants/index.json")
    plants = json.loads(response.text)
    return plants


def save_run_timestamp():
    """ Save timestap program was last run at """
    timestamp = datetime.now()
    pickle.dump(timestamp, open('last_db_update', 'wb'))


def fetch_all_plants():
    """ Fetch every plant from the Plantsolve API """
    plants = get_idex()

    for plant in plants:
        id = plant['id']
        slug = plant['slug']
        response = requests.get(f"https://www.plantsolve.com/api/v1/plants/{slug}.json")
        plant_data = json.loads(response.text)
        file_path = f'plants/{id}.json'
        plant['file_path'] = file_path
        json.dump(plant_data, open(file_path, 'w'), indent=4)

    # Save index file with paths of plant jsons
    json.dump(plants, open('plants/index.json', 'w'))

    save_run_timestamp()
