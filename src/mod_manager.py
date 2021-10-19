"""Manages the mods for the Crafter game."""


import json
import glob
import os
from pathlib import Path

from src.constants import DATA_DIR


def main():
    mods = ModManager.get_mod_list()
    print("Enabled:", ", ".join(mods["enabled"]))
    print("Disabled:", ", ".join(mods["disabled"]))


class ModManager:
    def __init__(self):
        if not os.path.exists(DATA_DIR / "mods"):
            mods_dir = DATA_DIR / "mods"
            os.mkdir(mods_dir)
            with open(mods_dir / "enabled.txt", "w") as f:
                f.write("# ExampleMod\n")
            with open(mods_dir / "ExampleMod.json", "w") as f:
                json.dump(
                    {
                        "meta": {
                            "name": "ExampleMod",
                            "version": "1.0.0",
                            "author": "ExampleAuthor",
                            "description": "Example mod description",
                        },
                        "items": [
                            {"name": "example material", "unlockable": False},
                            {
                                "name": "example item",
                                "unlockable": True,
                                "unlocked": False,
                                "crafting_recipe": ["example material", "water"],
                            },
                        ],
                    },
                    f,
                    indent=4,
                )
        self.loaded_mods = []
        self.add_new_mods()
        self.load_enabled_mods()

    @staticmethod
    def add_new_mods():
        """Adds new mods to the enabled.json file."""
        mods = ModManager.get_mod_list()
        new_mods = []
        files = glob.glob("mods/*.json")
        for file in files:
            if Path(file).stem not in mods["enabled"] + mods["disabled"]:
                new_mods.append((Path(file).stem))
        with open("mods/enabled.txt", "a") as mod_file:
            [mod_file.write("\n# " + mod) for mod in new_mods]
            pass

    @staticmethod
    def get_mod_list() -> dict:
        """A static method that returns a dictionary of all the mods enabled and disabled."""
        with open("mods/enabled.txt", "r") as mod_file:
            mods = {"enabled": [], "disabled": []}

            for line in mod_file.readlines():
                line = line.strip()
                if line.isspace() or line == "":
                    continue
                elif line.startswith("#"):
                    mods["disabled"].append(line.removeprefix("#").strip())
                else:
                    mods["enabled"].append(line)
        return mods

    def apply_loaded_mods(self, materials: list, recipes: dict[str, set[str]]):
        """Applies all loaded mods to the game."""
        for mod in self.loaded_mods:
            for item in mod["items"]:
                if not item["unlockable"]:
                    materials.append(item["name"])
                elif not item["unlocked"] and item["unlockable"]:
                    recipes[item["name"]] = set(item["crafting_recipe"])
                elif item["unlocked"] and item["unlockable"]:
                    recipes[item["name"]] = set(item["crafting_recipe"])
                    materials.append(item["name"])
        return materials, recipes

    def load_enabled_mods(self):
        enabled_mods = ModManager.get_mod_list()["enabled"]
        for mod in enabled_mods:
            self.load_mod(mod)

    def load_mod(self, name) -> bool:
        """Loads a mod. Returns True if the mod was loaded successfully."""
        if name == "enabled":
            return

        with open(f"mods/{name}.json") as f:
            mod_data: dict = json.load(f)

        meta: dict = mod_data.get("meta", None)

        if meta is None:
            print(f"Mod '{name}' is missing its metadata.")
            return False
        for mod in self.loaded_mods:
            if mod == mod_data:
                print(f"Mod '{name}' is already loaded.")
                return False

        self.loaded_mods.append(mod_data)
        print(f"Loaded mod '{name}' by {meta['author']}.")
        return True


if __name__ == "__main__":
    main()
