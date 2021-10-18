import enum
import os

import requests
import toml

from constants import *
from classes import *
from save_manager import save_game, load_game
from mod_manager import ModManager


raw_link = "https://github.com/C-ffeeStain/CrafterCLI/raw/main/"
releases_link = "https://api.github.com/repos/C-ffeeStain/CrafterCLI/releases"

settings = {"username": "Anonymous User", "password": "", "auto-update": True}


with open(PATH / "VERSION", "r") as f:
    version = f.read().splitlines()[0]
    online_version = requests.get(raw_link + "VERSION").text.splitlines()[0]
    if (
        version != online_version
        and not version.endswith("-beta")
        and settings["auto-update"]
    ):
        print("New version:", online_version)
        print("Updating...")
        releases = requests.get(releases_link)
        for release in releases.json():
            print("Online version:", online_version)
            print("Release:", release["tag_name"].strip())
            if release["tag_name"] == online_version:
                print("Downloading...")
                os.rename("Crafter.exe", "Crafter.backup.exe")
                r = requests.get(
                    release["assets"][0]["browser-download-url"],
                    allow_redirects=True,
                )

#                     print("Done!")
#             sys.exit(1)

if not os.path.exists("settings.cfg"):
    with open("settings.cfg", "w") as f:
        settings = {
            "username": input("Enter your username: "),
            "password": input("Enter your password: "),
            "auto-update": input("Auto-update? (y/n): ") == "y",
        }
        toml.dump(settings, f)

recipes = {
    "grass": {"dirt", "water"},
    "beach": {"sand", "water"},
    "desert": {"sand", "stone"},
    "mountain": {"stone", "stone"},
    "forest": {"wood", "grass"},
    "river": {"water", "stone"},
    "oasis": {"desert", "water"},
}

materials = ["water", "dirt", "sand", "stone", "ore", "seed", "wood"]

unlocked_items = load_game()
if not unlocked_items:
    unlocked_items = []

if __name__ == "__main__":
    print("Type 'materials' for a list of unlocked materials.")
    print(
        "To craft items, type 'craft' and then the list of materials separated by commas."
    )
    print("Example: craft sand,water")
    print("To exit, type 'exit'.")

    modman = ModManager()
    while True:
        instruction = input(">> ")
        split_instruction = instruction.split()
        command = split_instruction[0]
        args = [value.strip() for value in split_instruction[1:]]
        if command == "exit":
            break
        elif command == "materials":
            for material in materials:
                print(material)
        elif command == "craft":
            typed_materials = instruction.removeprefix(command + " ").split(",")
            for key, value in list(recipes.items()) + list(unlocked_items):
                if value == set(typed_materials):
                    print(f"You unlocked {key}!")
                    unlocked_items.append(key)
        elif command == "exit":
            save_game(unlocked_items)
            break
        else:
            print("Unknown command:", command)
