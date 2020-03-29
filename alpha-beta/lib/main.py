import numpy as np
import random
import math


class AlphaBeta:

    def __init__(self, board, no):
        self.board = board
        self.no = no    # Is AlphaBeta Player 1 or Player 2

    def minimax(self, board, depth, alpha, beta, maximising_Player):

        valid_location = Board.valid_locations(board)
        is_terminal = Board.terminal_node(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if Board.so_won(board, 2):
                    return (None, 100000)  # immer zwei Einträge weil ich Platz für Speichern der Spalte brauche
                elif Board.so_won(board, 1):
                    return (None, -100000)
                else:
                    return (None, 0)
            else:
                return (None, self.value_function(board, 2))

        if maximising_Player:
            score = -math.inf
            column = random.choice(valid_location)
            for selected_col in valid_location:
                row = Board.where_it_lands(board, selected_col)
                board_copy = board.copy()
                Board.play(board_copy, row, selected_col, 2)
                new_score = self.minimax(board_copy, depth - 1, alpha, beta, False)[1]
                if new_score > score:
                    score = new_score
                    column = selected_col
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            return column, score

        else:
            score = math.inf
            column = random.choice(valid_location)
            for selected_col in valid_location:
                row = Board.where_it_lands(board, selected_col)
                board_copy = board.copy()
                Board.play(board_copy, row, selected_col, 1)
                new_score = self.minimax(board_copy, depth - 1, alpha, beta, True)[1]
                if new_score < score:
                    score = new_score
                    column = selected_col
                beta = min(beta, score)
                if alpha >= beta:
                    break
            return column, score

    # returns a value of an action
    # values are abitrary....room for improvements?
    def value_function(self, board, piece):
        score = 0
        opp_piece = 3 - piece

        for r in range(6):
            # row_array = [int(i) for i in list(board[r, :])]   # not needed: set dtype=int during board initialisation
            row_array = board[r, :].tolist()
            for c in range(4):
                window = row_array[c:c + 4]
                if window.count(piece) == 4:
                    score += 100
                elif window.count(piece) == 3 and window.count(0) == 1:
                    score += 30
                elif window.count(piece) == 2 and window.count(0) == 2:
                    score += 10
                if window.count(opp_piece) == 3 and window.count(0) == 1:
                    score -= 31

        for c in range(7):
            # col_array = [int(i) for i in list(board[:, c])]
            col_array = board[:, c].tolist()
            for r in range(3):
                window = col_array[r:r + 4]
                if window.count(piece) == 4:
                    score += 100
                elif window.count(piece) == 3 and window.count(0) == 1:
                    score += 30
                elif window.count(piece) == 2 and window.count(0) == 2:
                    score += 10
                if window.count(opp_piece) == 3 and window.count(0) == 1:
                    score -= 31

        for r in range(3):
            for c in range(4):
                window = [board[r + i][c + i] for i in range(4)]
                if window.count(piece) == 4:
                    score += 100
                elif window.count(piece) == 3 and window.count(0) == 1:
                    score += 30
                elif window.count(piece) == 2 and window.count(0) == 2:
                    score += 10
                if window.count(opp_piece) == 3 and window.count(0) == 1:
                    score -= 31

        for r in range(3):
            for c in range(4):
                window = [board[r + 3 - i][c + i] for i in range(4)]
                if window.count(piece) == 4:
                    score += 100
                elif window.count(piece) == 3 and window.count(0) == 1:
                    score += 30
                elif window.count(piece) == 2 and window.count(0) == 2:
                    score += 10
                if window.count(opp_piece) == 3 and window.count(0) == 1:
                    score -= 31

        return score


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


if __name__ == '__main__':

    board = Board.build_board()
    print(board)
    print("============\n")

    over = False
    turn = 0

    AB = AlphaBeta(board, no=2)

    while not over:
        # NEED TO HANDLE DRAWS!
        # Human
        if turn == 0:
            print("Human:")
            selected_col = int(input("P1 choose (0-6):"))
            if Board.legal_check(board, selected_col):
                row = Board.where_it_lands(board, selected_col)
                Board.play(board, row, selected_col, 1)

                if Board.so_won(board, 1):
                    print("Human wins. Congratulations, John Henry.")
                    over = True
            # If illegal column is selected, ask the user again. => Outsourcing in function necessary
            else:
                print("Selected illegal column. Idiot! GAME OVER!")
                break

        # Alphabeta
        else:
            print("Alphabeta:")
            selected_col, minimax_score = AB.minimax(board, 3, -math.inf, math.inf, True)
            if Board.legal_check(board, selected_col):
                row = Board.where_it_lands(board, selected_col)
                Board.play(board, row, selected_col, 2)

                if Board.so_won(board, 2):
                    print("AI wins. Death to humanity!")
                    over = True

        Board.print_right_way(board)
        print("============\n")

        turn ^= 1
