import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"


def _load_json(filename):
    file_path = DATA_DIR / filename
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_distance_matrix():
    return _load_json("distance_matrix.json")["adjacency_matrix_13x13"]


def load_customers():
    return _load_json("customers.json")["locations"]


def load_scenario(scenario_name):
    scenarios = _load_json("scenarios.json")
    return scenarios[scenario_name]
