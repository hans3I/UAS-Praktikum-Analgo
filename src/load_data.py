import json

def load_distance_matrix():
    with open("../data/distance_matrix.json", "r", encoding="utf-8") as file:
        return json.load(file)["adjacency_matrix_13x13"]


def load_customers():
    with open("../data/customers.json", "r", encoding="utf-8") as file:
        return json.load(file)["locations"]


def load_scenario(scenario_name):
    with open("../data/scenarios.json", "r", encoding="utf-8") as file:
        scenarios = json.load(file)

    return scenarios[scenario_name]
