import numpy as np

class Board:

    # initialise board
    @staticmethod
    def build_board():
        board = np.zeros((6, 7), dtype=int)
        return board

    # flip the board
    @staticmethod
    def print_right_way(board):
        print(np.flip(board, 0))

    # checks if colums are legal to be played; True if legal
    @staticmethod
    def legal_check(board, selected_col):
        return board[5][selected_col] == 0

    # gives the row where piece lands
    @staticmethod
    def where_it_lands(board, selected_col):
        for r in range(6):
            if board[r][selected_col] == 0:
                return r

    # changes matrix entry
    @staticmethod
    def play(board, row, selected_col, piece):
        board[row][selected_col] = piece

    # determines if there is a winner
    @staticmethod
    def so_won(board, piece):
        for c in range(4):
            for r in range(6):
                if all(x == piece for x in [board[r][c], board[r][c + 1], board[r][c + 2], board[r][c + 3]]):
                    return True
        for c in range(7):
            for r in range(3):
                if all(x == piece for x in [board[r][c], board[r + 1][c], board[r + 2][c], board[r + 3][c]]):
                    return True
        for c in range(4):
            for r in range(3):
                if all(x == piece for x in [board[r][c], board[r + 1][c + 1], board[r + 2][c + 2], board[r + 3][c + 3]]):
                    return True
        for c in range(4):
            for r in range(3, 6):
                if all(x == piece for x in [board[r][c], board[r - 1][c + 1], board[r - 2][c + 2], board[r - 3][c + 3]]):
                    return True

    # determines if node is a terminal node
    @staticmethod
    def terminal_node(board):
        return any([Board.so_won(board, piece=1), Board.so_won(board, piece=2), len(Board.valid_locations(board)) == 0])

    # returns list of possible next locations
    @staticmethod
    def valid_locations(board):
        locations = []
        for selected_col in range(7):
            if Board.legal_check(board, selected_col):
                locations.append(selected_col)

        return locations