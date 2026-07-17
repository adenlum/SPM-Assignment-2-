import json
import os

from building_types import Residential, Industry, Commercial, Park, Road
from grid import Grid

# maps the symbol stored on disk back to the actual Building class
SYMBOL_TO_CLASS = {
    "R": Residential,
    "I": Industry,
    "C": Commercial,
    "O": Park,
    "*": Road,
}

SAVE_FOLDER = "saves"


def save_game(filename, grid, mode, **state):
    """Saves the grid and any extra game state (coins, turn, score, etc.) to a JSON file.
    :param filename: name to save the file as (no extension needed)
    :param grid: the current Grid object
    :param mode: "arcade" or "freeplay", so load_game knows where to resume
    :param state: any extra values to remember (coins=16, turn=3, score=10, ...)
    """
    os.makedirs(SAVE_FOLDER, exist_ok=True)

    data = {
        "mode": mode,
        "size": grid.size,
        "board": [
            [cell.symbol if cell is not None else None for cell in row]
            for row in grid.data
        ],
        "state": state,
    }

    path = os.path.join(SAVE_FOLDER, f"{filename}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    return path


def load_game(filename):
    """Loads a previously saved game.
    :returns: (mode, grid, state) so the caller can resume the right mode with the right values
    :raises FileNotFoundError: if no save file with that name exists
    """
    path = os.path.join(SAVE_FOLDER, f"{filename}.json")

    with open(path, "r") as f:
        data = json.load(f)

    grid = Grid(size=data["size"])

    for r, row in enumerate(data["board"]):
        for c, symbol in enumerate(row):
            if symbol is not None:
                building_class = SYMBOL_TO_CLASS[symbol]
                grid.data[r][c] = building_class()

    return data["mode"], grid, data["state"]


def list_saves():
    """Lists the names of all available save files (without the .json extension).
    :returns: a list of save names, empty if the saves folder doesn't exist or has no saves
    """
    if not os.path.isdir(SAVE_FOLDER):
        return []

    return [
        os.path.splitext(f)[0]
        for f in os.listdir(SAVE_FOLDER)
        if f.endswith(".json")
    ]
