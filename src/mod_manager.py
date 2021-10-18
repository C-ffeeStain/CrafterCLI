"""Manages the mods for the Crafter game."""


import json
import glob
from pathlib import Path


def main():
    mod_list = ModManager.get_mod_list()
    print("Enabled:", ", ".join(mod_list["enabled"]))
    print("Disabled:", ", ".join(mod_list["disabled"]))


class ModManager:
    def __init__(self):
        self.loaded_mods = []
        self.add_new_mods()
        self.load_enabled_mods()

    @staticmethod
    def get_mod_list():
        """Returns a list of all the mods enabled and disabled."""
        with open("mods/enabled.json", "r") as mod_file:
            data = json.load(mod_file)
            mod_list = data["enabled"] + data["disabled"]
        files = glob.glob("mods/*.json")
        for file in files:
            if Path(file).stem not in mod_list:
                data["disabled"].append((Path(file).stem))
        with open("mods/enabled.json", "w") as mod_file:
            json.dump(data, mod_file, indent=4)

    def add_new_mods(self):
        """Adds new mods to the enabled.json file."""
        with open("mods/enabled.json", "r") as mod_file:
            data = json.load(mod_file)
            enabled_mods = data["enabled"]
            for mod in enabled_mods:
                self.load_mod(mod)

    def load_enabled_mods(self):
        enabled_mods = ModManager.get_mod_list()["enabled"]
        for mod in enabled_mods:
            self.load_mod(mod)

    def create_mod_guid(self, meta):
        """Creates a GUID for a mod in the format of `author.modname`."""
        return f"{meta['author'].lower().replace(' ', '_')}.{meta['name'].lower().replace(' ', '_')}"

    def load_mod(self, name) -> bool:
        """Loads a mod. Returns true if the mod was loaded successfully."""

        with open(f"mods/{name}.json") as f:
            mod_data: dict = json.load(f)

        meta: dict = mod_data.get("meta", None)

        if meta is None:
            print(f"Mod '{name}' is missing its metadata.")
            return False
        for mod in self.loaded_mods:
            if mod == self.create_mod_guid(meta):
                print(f"Mod '{name}' is already loaded.")
                return False

        self.loaded_mods.append(self.create_mod_guid(meta))
        print(f"Loaded mod '{name}' by {meta['author']}.")
        return True


if __name__ == "__main__":
    main()
