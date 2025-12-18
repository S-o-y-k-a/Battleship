import numpy as np

import random

bot_state = {
    "mode": "RANDOM",
    "hits": [],
    "axis": None
}

COLORS = {
    "reset": "\033[0m",
    "white": "\033[97m",
    "gray": "\033[90m",
    "red": "\033[91m",
    "blue": "\033[94m",
}

LETTERS = "ABCDEFGHIJ"
LETTER_TO_IDX = {letter: i for i, letter in enumerate(LETTERS)}


def print_board(board: np.ndarray, show_ships: bool):

    print(" " + "".join(str(i + 1).rjust(2) for i in range(10)))

    for i in range(10):
        row = [LETTERS[i]]

        for j in range(10):
            cell = board[i, j]

            if cell == 0:
                row.append(f"{COLORS['white']}·{COLORS['reset']}")

            elif cell == 1:
                if show_ships:
                    row.append(f"{COLORS['gray']}■{COLORS['reset']}")
                else:
                    row.append(f"{COLORS['white']}·{COLORS['reset']}")

            elif cell == -1:
                row.append(f"{COLORS['white']}×{COLORS['reset']}")

            elif cell == 2:
                row.append(f"{COLORS['red']}×{COLORS['reset']}")

            elif cell == 3:
                row.append(f"{COLORS['blue']}○{COLORS['reset']}")

        print(" ".join(row))


def print_player_board(board: np.ndarray):
    print("\nВаша доска:")
    print_board(board, show_ships=True)


def print_enemy_board(board: np.ndarray):
    print("\nДоска противника:")
    print_board(board, show_ships=False)

def bot_choose_move(board, bot_state, available_cells):
    if bot_state["mode"] == "RANDOM":
        return random.choice(list(available_cells))

    elif bot_state["mode"] == "TARGET":
        x0, y0 = bot_state["hits"][0]
        candidates = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x0 + dx, y0 + dy
            if 0 <= nx < 10 and 0 <= ny < 10:
                if board[nx, ny] not in (2,3,-1):
                    candidates.append((nx, ny))
        if candidates:
            return random.choice(candidates)
        else:
            bot_state["mode"] = "RANDOM"
            return random.choice(list(available_cells))

    elif bot_state["mode"] == "AXIS":
        hits = sorted(bot_state["hits"])
        if bot_state["axis"] == "H":
            row = hits[0][0]
            min_col = min(y for x,y in hits)
            max_col = max(y for x,y in hits)
            if min_col-1 >= 0 and board[row, min_col-1] not in (2,3,-1):
                return row, min_col-1
            if max_col+1 < 10 and board[row, max_col+1] not in (2,3,-1):
                return row, max_col+1
        elif bot_state["axis"] == "V":
            col = hits[0][1]
            min_row = min(x for x,y in hits)
            max_row = max(x for x,y in hits)
            if min_row-1 >= 0 and board[min_row-1, col] not in (2,3,-1):
                return min_row-1, col
            if max_row+1 < 10 and board[max_row+1, col] not in (2,3,-1):
                return max_row+1, col
        bot_state["mode"] = "RANDOM"
        bot_state["hits"] = []
        bot_state["axis"] = None
        return random.choice(list(available_cells))

def bot_process_result(bot_state, x, y, result, ship_destroyed_flag):
    if result == "hit":
        if not bot_state["hits"]:
            bot_state["hits"].append((x,y))
            bot_state["mode"] = "TARGET"
        else:
            bot_state["hits"].append((x,y))
            if bot_state["mode"] == "TARGET":
                x0, y0 = bot_state["hits"][0]
                if x0 == x:
                    bot_state["axis"] = "H"
                else:
                    bot_state["axis"] = "V"
                bot_state["mode"] = "AXIS"
    if ship_destroyed_flag:
        bot_state["hits"] = []
        bot_state["axis"] = None
        bot_state["mode"] = "RANDOM"