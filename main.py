import os
import toml
import sys
import requests

raw_link = "https://github.com/C-ffeeStain/CrafterCLI/raw/main/"

settings = {
    "username": "Anonymous User",
    "password": "",
    "auto-update": True
}

with open("VERSION", "r") as f:
    version = f.read().strip()
    online_version = requests.get(raw_link + "VERSION").text
    if version != online_version and not version.endswith("-beta") and settings["auto-update"]:
        print("Old version:", version)
        print("New version:", online_version)
        print("Update available")
        sys.exit(1)

if not os.path.exists("settings.cfg"):
    with open("settings.cfg", "w") as f:
        settings = {
            "username": input("Enter your username: "),
            "password": input("Enter your password: "),
            "auto-update": input("Auto-update? (y/n): ") == "y"

        }
        toml.dump(settings, f)

if __name__ == "__main__":
    print("Hello, this is a test for the auto-updater I am adding.")
