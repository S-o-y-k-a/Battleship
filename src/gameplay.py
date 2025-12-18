import numpy as np
import csv
import os
import random
import re

from src.utils import print_player_board, print_enemy_board

Letters = {"A": 0, "B": 1, "C": 2,
               "D": 3, "E": 4, "F": 5,
               "G": 6, "H": 7, "I": 8,
               "J": 9}

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "game_state.csv"
)

def all_ships_destroyed(board):
    return not np.any(board == 1)

def parse_coords(move: str):
    if not move:
        return None

    move = move.strip().upper()

    match = re.fullmatch(r"([A-J])(10|[1-9])", move)
    if not match:
        return None

    letter, number = match.groups()
    x = Letters[letter]
    y = int(number) - 1

    return x, y

def shoot(board, x, y):

    if board[x, y] in (2, 3, -1):
        return "repeat"

    if board[x, y] == 1:
        board[x, y] = 2
        return "hit"
    else:
        board[x, y] = 3
        return "miss"


def ship_destroyed(board, x, y):
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        cx, cy = x + dx, y + dy
        while 0 <= cx < 10 and 0 <= cy < 10:
            if board[cx, cy] == 1:
                return False
            if board[cx, cy] in (0, 3, -1):
                break
            cx += dx
            cy += dy
    return True


def mark_around_destroyed(board, x, y):

    stack = [(x, y)]
    visited = set()

    while stack:
        cx, cy = stack.pop()
        visited.add((cx, cy))

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < 10 and 0 <= ny < 10:
                if board[nx, ny] == 2 and (nx, ny) not in visited:
                    stack.append((nx, ny))

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < 10 and 0 <= ny < 10:
                    if board[nx, ny] == 0:
                        board[nx, ny] = -1


def write_csv(turn, p_move, p_res, b_move, b_res, player_board, bot_board):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

    with open(DATA_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            turn,
            p_move, p_res,
            b_move, b_res,
            player_board.tolist(),
            bot_board.tolist()
        ])


def game_loop(player_board, bot_board):
    turn = 1

    with open(DATA_PATH, "w", newline="") as f:
        csv.writer(f).writerow([
            "turn",
            "player_move", "player_result",
            "bot_move", "bot_result",
            "player_board", "bot_board"
        ])

    while True:
        print(f"\n--- ХОД {turn} ---")

        print_enemy_board(bot_board)
        move = input("Ваш ход (например A5): ").upper()
        parsed = parse_coords(move)

        if not parsed:
            print("Неверный ввод :p")
            continue

        px, py = parsed
        p_res = shoot(bot_board, px, py)
        if p_res == "repeat":
            print("А сюда стрелять не стоит, давайте заново :p")
            continue

        if p_res == "hit" and ship_destroyed(bot_board, px, py):
            mark_around_destroyed(bot_board, px, py)

        while True:
            bx, by = random.randint(0, 9), random.randint(0, 9)
            b_res = shoot(player_board, bx, by)
            if b_res != "repeat":
                break

        if b_res == "hit" and ship_destroyed(player_board, bx, by):
            mark_around_destroyed(player_board, bx, by)

        write_csv(
            turn,
            move, p_res,
            f"{bx},{by}", b_res,
            player_board,
            bot_board
        )

        print_player_board(player_board)
        print_enemy_board(bot_board)

        if all_ships_destroyed(bot_board):
            print("Ура победа!!!")
            break

        if all_ships_destroyed(player_board):
            print("Будь ты проклят, Перри утконос! Робот победил...")
            break

        turn += 1