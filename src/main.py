import os
import sys
from platform import system
from time import sleep
from enum import Enum

import requests
import toml

from constants import *
from mod_manager import ModManager
from save_manager import load_game, save_game


class UnlockedMaterials(Enum):
    Grass = 1
    Beach = 2
    Desert = 4
    Mountain = 8
    Forest = 16
    River = 32
    Oasis = 64


def get_password():
    confirmed = False
    while not confirmed:
        password = input("Enter your password: ")
        password_confirm = input("Confirm your password: ")
        if password == password_confirm:
            confirmed = True
        else:
            print("Passwords do not match.")
    return password


raw_link = "https://github.com/C-ffeeStain/CrafterCLI/raw/main/"
releases_link = "https://api.github.com/repos/C-ffeeStain/CrafterCLI/releases"

settings = {"username": "Anonymous User", "password": "", "auto-update": True}

if not os.path.exists("settings.cfg"):
    with open("settings.cfg", "w") as f:
        settings = {
            "username": input("Enter your username: "),
            "password": get_password(),
            "auto-update": input("Auto-update? (y/n): ") == "y",
        }
        toml.dump(settings, f)
else:
    with open("settings.cfg", "r") as f:
        settings = toml.load(f)

if settings["password"] != "":
    incorrect_password = True
    attempts = 5
    while incorrect_password:
        if attempts == 0:
            print("You have exceeded the maximum number of attempts.")
            sys.exit()
        password = input("Enter your password: ")
        if password != settings["password"]:
            print("Incorrect password.")
            attempts -= 1
        else:
            incorrect_password = False

# with open(PATH / "VERSION", "r") as f:
#     version = f.read().splitlines()[0]
#     online_version = requests.get(raw_link + "VERSION").text.splitlines()[0]
#     if (
#         version != online_version
#         and not version.endswith("-beta")
#         and settings["auto-update"]
#     ):
#         print("New version:", online_version)
#         if settings["auto_update"]:
#             print("Updating...")
#             releases = requests.get(releases_link)
#             for release in releases.json():
#                 print("Online version:", online_version)
#                 print("Release:", release["tag_name"].strip())
#                 if release["tag_name"] == online_version:
#                     print("Downloading...")
#                     os.rename(__file__, "Crafter.backup.exe")
#                     r = requests.get(
#                         release["assets"][0]["browser-download-url"],
#                         allow_redirects=True,
#                     )

#                     print("Done!")
#             sys.exit(1)


recipes = {
    "grass": {"dirt", "water"},
    "beach": {"sand", "water"},
    "desert": {"sand", "stone"},
    "mountain": {"stone", "ore"},
    "forest": {"wood", "grass"},
    "river": {"water", "stone"},
    "oasis": {"desert", "water"},
}

materials = ["water", "dirt", "sand", "stone", "ore", "seed", "wood"]

unlocked_items = load_game()
if not unlocked_items:
    unlocked_items = []

if __name__ == "__main__":
    sys_name = system()
    if sys_name == "Windows":
        os.system("title Crafter")

    modman = ModManager()
    materials, recipes = modman.apply_loaded_mods(materials, recipes)

    print("\nType 'materials' for a list of unlocked materials.")
    print(
        "To craft items, type 'craft' and then the list of materials separated by commas."
    )
    print("Example: craft sand,water")
    print("To exit, type 'exit'.")
    sleep(2.5)
    while True:
        if sys_name == "Windows":
            os.system("cls")
        else:
            os.system("clear")
        instruction = input(">> ")
        if instruction == "":
            continue
        split_instruction = instruction.split()
        command = split_instruction[0]
        args = [value.strip() for value in split_instruction[1:]]
        if command == "exit":
            break
        elif command == "materials":
            for material in materials:
                print(material)
            input("Press enter to continue...")
        elif command == "craft":
            typed_materials = instruction.removeprefix(command + " ").split(",")
            for key, value in recipes.items():
                if value == set(typed_materials) and key not in materials:
                    print(f"You unlocked {key}!")
                    materials.append(key)
                    sleep(1.75)
        elif command == "exit":
            save_game(materials)
            break
        else:
            print("Unknown command:", command)
