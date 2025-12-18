import numpy as np
import re
import os

from src import utils as ut

letters = {"A": 0, "B": 1, "C": 2,
               "D": 3, "E": 4, "F": 5,
               "G": 6, "H": 7, "I": 8,
               "J": 9}

def place_ship(board, x1, y1, x2, y2):
    size = max(abs(x2 - x1), abs(y2 - y1)) + 1
    dx = np.sign(x2 - x1)
    dy = np.sign(y2 - y1)

    for i in range(size):
        board[x1 + dx * i, y1 + dy * i] = 1

    return size

def is_valid_placement(board, x1, y1, x2, y2):
    if x1 != x2 and y1 != y2:
        return False

    size = max(abs(x2 - x1), abs(y2 - y1)) + 1
    print(size)
    dx = np.sign(x2 - x1)
    dy = np.sign(y2 - y1)

    for i in range(size):
        x = x1 + dx * i
        y = y1 + dy * i

        if board[x, y] != 0:
            return False

        for cx in range(x - 1, x + 2):
            for cy in range(y - 1, y + 2):
                if 0 <= cx < 10 and 0 <= cy < 10:
                    if board[cx, cy] != 0 and (cx, cy) != (x, y):
                        return False

    return size

def to_coords_h(cell):
        x = cell[0]
        y = int(cell[1:]) - 1

        if x not in letters or not (0 <= y < 10):
            return None

        return letters[x], y

def to_coords(s):
    match = re.fullmatch(r"\s*([A-J]\d{1,2})\s+([A-J]\d{1,2})\s*", s.upper())
    if not match:
        return None

    start = to_coords_h(match.group(1))
    end = to_coords_h(match.group(2))

    if start is None or end is None:
        return None

    return start, end
    
    
    


def create_board():

    ships = np.array([4, 3, 3, 2, 2, 2, 1, 1, 1, 1])
    board = np.zeros((10, 10), dtype=int)
    


    while ships.size > 0:

        print("Оставшиеся корабли:", ships)
        ship_coords = str(input("Введите координаты корабля (например A1 A3):"))

        parsed = to_coords(ship_coords)

        if not parsed:
            print("Неверный формат ввода :(")
            continue

        (x1, y1), (x2, y2) = parsed

        size = is_valid_placement(board, x1, y1, x2, y2)
        if not size:
            print("Неверное размещение :/")
            continue

        if size not in ships:
            print(f"Корабля размера {size} не может быть :)")
            continue

        place_ship(board, x1, y1, x2, y2)

        ut.print_board(board, True)

        idx = np.where(ships == size)[0]
        ships = np.delete(ships, idx[0])

    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, "data", "player_ships.csv")

    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    np.savetxt(data_path, board, fmt="%d", delimiter=",")

    return board