import math

from lib.main import Board, AlphaBeta
from lib.mcts import MCTS

if __name__ == '__main__':

    board = Board.build_board()
    print(board)
    print("============\n")

    over = False
    turn = 0

    M = MCTS(board, no=1)
    AB = AlphaBeta(board, no=2)

    while not over:

        # MCTS
        if turn == 0:
            # get the best move
            print("MCTS:")
            selected_col = M.selection(board=board)
            row = Board.where_it_lands(board, selected_col)
            Board.play(board, row, selected_col, 1)

            if Board.so_won(board, 2):
                print("MCTS wins!")
                over = True

        # Alpahbeta
        else:
            print("Alphabeta:")
            selected_col, minimax_score = AB.minimax(board, 3, -math.inf, math.inf, True)

            if Board.legal_check(board, selected_col):
                row = Board.where_it_lands(board, selected_col)
                Board.play(board, row, selected_col, 2)

                if Board.so_won(board, 2):
                    print("Alphabeta wins!")
                    over = True

        Board.print_right_way(board)
        print("============\n")

        turn ^= 1
