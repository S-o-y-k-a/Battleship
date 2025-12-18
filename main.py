from src.ship_input import create_board
from src.bot_generation import create_bot_board
from src.utils import print_board
from src.gameplay import game_loop

def main():

    player_board = create_board()
    bot_board = create_bot_board()

    game_loop(player_board, bot_board)

if __name__ == "__main__":
    main()