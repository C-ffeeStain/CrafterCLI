import json
import os

from constants import DATA_DIR


def save_game(game_data):
    """
    Saves the game data to a json file.
    """
    with open("save.json", "w") as save_file:
        json.dump(game_data, save_file)


def load_game():
    """
    Loads the game data from a json file.
    """
    if not os.path.exists("save.json"):
        return None
    with open("save.json", "r") as save_file:
        return json.load(save_file)
