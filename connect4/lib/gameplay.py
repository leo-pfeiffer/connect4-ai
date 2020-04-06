import math
from lib.board import Board
from lib.players import Human, AlphaBeta, MCTS


def play_game(players, board):

    should_print = __name__ == '__main__'

    if should_print:
        print(board)
        print("============\n")

    turn = 0

    while not Board.so_won(board, players[turn ^ 1].no) and len(Board.valid_locations(board)) > 0:
        if should_print:
            print("{}:".format(players[turn].name))
        selected_col = players[turn].selector(board, -math.inf, math.inf, True)

        if Board.legal_check(board, selected_col):
            row = Board.where_it_lands(board, selected_col)
            Board.play(board, row, selected_col, players[turn].no)

        if should_print:
            Board.print_right_way(board)
            print("============\n")

        turn ^= 1

    if Board.so_won(board, players[turn ^ 1].no):
        print("VICTORY FOR " + players[turn ^ 1].name)
        return players[turn ^ 1].name
    else:
        print("DRAW")
        return 'DRAW'


if __name__ == '__main__':
    board = Board.build_board()

    H1 = Human(board, no=1, name='Leo')
    H2 = Human(board, no=1, name='Elham')

    AB1 = AlphaBeta(board, no=1, name='Alphabeta1', depth=3)
    AB2 = AlphaBeta(board, no=2, name='Alphabeta2', depth=3)

    M1 = MCTS(board, no=1, name='MCTS1')
    M2 = MCTS(board, no=2, name='MCTS2')

    players = [M1, M2]

    play_game(players, board)       # do this to play game
