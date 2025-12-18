from src import ship_input as sh

import numpy as np

import random

import os
 

def create_bot_board():
    ships = np.array([4, 3, 3, 2, 2, 2, 1, 1, 1, 1])
    board = np.zeros((10, 10), dtype=int)

    while ships.size > 0:
        size = random.choice(ships)

        x = random.randint(0, 9)
        y = random.randint(0, 9)

        direction = random.choice(["h", "v"])

        if direction == "h":
            x1, y1 = x, y
            x2, y2 = x, y + size - 1
        else:
            x1, y1 = x, y
            x2, y2 = x + size - 1, y

        if not (0 <= x2 < 10 and 0 <= y2 < 10):
            continue

        if not sh.is_valid_placement(board, x1, y1, x2, y2):
            continue

        sh.place_ship(board, x1, y1, x2, y2)

        idx = np.where(ships == size)[0]
        ships = np.delete(ships, idx[0])

    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, "data", "bot_ships.csv")

    os.makedirs(os.path.dirname(data_path), exist_ok=True)

    np.savetxt(data_path, board, fmt="%d", delimiter=",")

    return board