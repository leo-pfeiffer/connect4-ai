import math

from lib.main import build_board, legal_check, where_it_lands, play, so_won, print_right_way, minimax
from lib.mcts import MCTS

if __name__ == '__main__':

    board = build_board()
    print(board)
    print("============\n")

    over = False
    turn = 0

    M = MCTS(board, no=1)

    while not over:

        # MCTS
        if turn == 0:
            # get the best move
            print("MCTS:")
            selected_col = M.selection(board=board)
            row = where_it_lands(board, selected_col)
            play(board, row, selected_col, 1)

            if so_won(board, 2):
                print("MCTS wins!")
                over = True

        # Alpahbeta
        else:
            print("Alphabeta:")
            selected_col, minimax_score = minimax(board, 3, -math.inf, math.inf, True)
            if legal_check(board, selected_col):
                row = where_it_lands(board, selected_col)
                play(board, row, selected_col, 2)

                if so_won(board, 2):
                    print("Alphabeta wins!")
                    over = True

        print_right_way(board)
        print("============\n")

        turn ^= 1
