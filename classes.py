import enum


class Recipe:
    ingredients = []


class Ingredient(enum.IntEnum):
    Water = 0
    Sand = 1
    Dirt = 2
    Stone = 3
    Wood = 4
    Grass = 5
    Beach = 6
    Metal = 7
    RustyMetal = 8
