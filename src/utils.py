import numpy as np

COLORS = {
    "reset": "\033[0m",
    "white": "\033[97m",
    "gray": "\033[90m",
    "red": "\033[91m",
    "blue": "\033[94m",
}

LETTERS = "ABCDEFGHIJ"


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