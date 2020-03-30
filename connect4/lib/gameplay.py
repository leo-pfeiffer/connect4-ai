import math
from lib.board import Board
from lib.players import AlphaBeta, MCTS, Human

if __name__ == '__main__':

    board = Board.build_board()
    print(board)
    print("============\n")

    turn = 0

    H1 = Human(board, no=1, name='John Henry')
    H2 = Human(board, no=1, name='Django')
    AB1 = AlphaBeta(board, no=1, name='Alphabeta1')
    AB2 = AlphaBeta(board, no=2, name='Alphabeta2')
    M1 = MCTS(board, no=1, name='MCTS1')
    M2 = MCTS(board, no=1, name='MCTS2')

    players = [AB1, M1]

    while not Board.so_won(board, players[turn ^ 1].no) and len(Board.valid_locations(board)) > 0:

        print("{}:".format(players[turn].name))
        selected_col = players[turn].selector(board, 3, -math.inf, math.inf, True)

        if Board.legal_check(board, selected_col):
            row = Board.where_it_lands(board, selected_col)
            Board.play(board, row, selected_col, players[turn].no)

        Board.print_right_way(board)
        print("============\n")

        turn ^= 1

    if Board.so_won(board, players[turn ^ 1].no):
        print("VICTORY FOR " + players[turn ^ 1].name)
    else:
        print("DRAW")
