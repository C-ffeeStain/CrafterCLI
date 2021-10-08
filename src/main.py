import enum
import os

import requests
import toml

from constants import *


class UnlockedMaterials(enum.Enum):
    Grass = 1
    Beach = 2
    Desert = 4
    Mountain = 8
    Forest = 16
    River = 32


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
    "Grass": {"dirt", "water"},
    "Beach": {"sand", "water"},
    "Desert": {"sand", "rock"},
    "Mountain": {"rock", "rock"},
    "Forest": {"wood", "grass"},
    "River": {"water", "rock"},
}

materials = ["water", "dirt", "sand", "stone", "ore", "seed"]

if __name__ == "__main__":
    print("Type 'materials' for a list of unlocked materials.")
    print(
        "To craft items, type 'craft' and then the list of materials separated by commas."
    )
    print("Example: craft sand,water")
    print("To exit, type 'exit'.")
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
            for key, value in recipes.items():
                if value == set(typed_materials):
                    print(key)
        elif command == "exit":
            break
        else:
            print("Unknown command:", command)
