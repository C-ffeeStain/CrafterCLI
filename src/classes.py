"""Contains all the classes required for any part of the game."""


import enum


class UnlockedMaterials(enum.Enum):
    Grass = 1
    Beach = 2
    Desert = 4
    Mountain = 8
    Forest = 16
    River = 32


class Material:
    def __init__(
        self,
        id: int,
        name: str = "NO NAME",
        item: bool = False,
        unlocked: bool = False,
        crafting_recipe: set = None,
    ):
        """A Crafter material.\n
        Parameters:
            id (int): id for internal game functions
            name (str): name that the user will see, defaults to "NO NAME"
            item (bool): if the material is an craftable item, defaults to False
            unlocked (bool): if the material is unlocked, defaults to False
            crafting_recipe (set): a set of material names that craft this material, defaults to None
        """
        self.id = id
        self.name = name
        self.item = item
        if item and crafting_recipe is None:
            raise ValueError(f"Item {item} must have a crafting recipe.")

        self.unlocked = unlocked
        self.crafting_recipe = crafting_recipe

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class Game:
    def __init__(self, unlocked_materials: list):
        """The game class.\n
        Parameters:
            unlocked_materials (list): a set of unlocked materials
        """
        self.materials = [
            Material(0, "water", item=False, unlocked=True),
            Material(1, "dirt", item=False, unlocked=True),
            Material(2, "sand", item=False, unlocked=True),
            Material(3, "stone", item=False, unlocked=True),
            Material(4, "ore", item=False, unlocked=True),
            Material(5, "seed", item=False, unlocked=True),
            Material(6, "wood", item=False, unlocked=True),
            Material(
                7, "grass", item=True, unlocked=False, crafting_recipe={"water", "dirt"}
            ),
            Material(
                8, "beach", item=True, unlocked=False, crafting_recipe={"water", "sand"}
            ),
            Material(
                9,
                "desert",
                item=True,
                unlocked=False,
                crafting_recipe={"sand", "stone"},
            ),
            Material(
                10,
                "mountain",
                item=True,
                unlocked=False,
                crafting_recipe={"stone", "stone"},
            ),
            Material(
                11,
                "forest",
                item=True,
                unlocked=False,
                crafting_recipe={"grass", "grass"},
            ),
        ]
