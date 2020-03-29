import numpy as np
import random
import math


# initialise board
def build_board():
    board = np.zeros((6, 7), dtype=int)
    return board


# flip the board
def print_right_way(board):
    print(np.flip(board, 0))


# checks if colums are legal to be played; True if legal
def legal_check(board, selected_col):
    return board[5][selected_col] == 0


# gives the row where piece lands
def where_it_lands(board, selected_col):
    for r in range(6):
        if board[r][selected_col] == 0:
            return r


# changes matrix entry
def play(board, row, selected_col, piece):
    board[row][selected_col] = piece


# determines if there is a winner
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


# returns a value of an action
# values are abitrary....room for improvements?
def value_function(board, piece):
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


# determines if node is a terminal node
def terminal_node(board):
    return any([so_won(board, piece=1), so_won(board, piece=2), len(valid_locations(board)) == 0])


# alpha-beta aufbauend auf Pseudocode Wikipedia
def minimax(board, depth, alpha, beta, maximising_Player):

    valid_location = valid_locations(board)
    is_terminal = terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if so_won(board, 2):
                return (None, 100000)  # immer zwei Einträge weil ich Platz für Speichern der Spalte brauche
            elif so_won(board, 1):
                return (None, -100000)
            else:
                return (None, 0)
        else:
            return (None, value_function(board, 2))
    if maximising_Player:
        score = -math.inf
        column = random.choice(valid_location)
        for selected_col in valid_location:
            row = where_it_lands(board, selected_col)
            board_copy = board.copy()
            play(board_copy, row, selected_col, 2)
            new_score = minimax(board_copy, depth - 1, alpha, beta, False)[1]
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
            row = where_it_lands(board, selected_col)
            board_copy = board.copy()
            play(board_copy, row, selected_col, 1)
            new_score = minimax(board_copy, depth - 1, alpha, beta, True)[1]
            if new_score < score:
                score = new_score
                column = selected_col
            beta = min(beta, score)
            if alpha >= beta:
                break
        return column, score


# returns list of possible next locations
def valid_locations(board):
    locations = []
    for selected_col in range(7):
        if legal_check(board, selected_col):
            locations.append(selected_col)

    return locations


if __name__ == '__main__':

    board = build_board()
    print(board)

    over = False
    turn = 0

    while not over:
        # NEED TO HANDLE DRAWS!
        # Human
        if turn == 0:
            selected_col = int(input("P1 choose (0-6):"))
            if legal_check(board, selected_col):
                row = where_it_lands(board, selected_col)
                play(board, row, selected_col, 1)

                if so_won(board, 1):
                    print("P1 wins")
                    over = True
            # If illegal column is selected, ask the user again. => Outsourcing in function necessary
            else:
                print("Selected illegal column. Idiot! GAME OVER!")
                break

        # AI
        else:

            selected_col, minimax_score = minimax(board, 3, -math.inf, math.inf, True)
            if legal_check(board, selected_col):
                row = where_it_lands(board, selected_col)
                play(board, row, selected_col, 2)

                if so_won(board, 2):
                    print("AI wins")
                    over = True

        print_right_way(board)

        turn ^= 1
