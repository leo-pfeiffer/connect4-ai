import numpy as np
import random


# initialise board
def build_board():
    board=np.zeros((6,7))
    return board
board=build_board()
print(board)
#needed tu turn the board the right way round
def print_right_way (board):
    print(np.flip(board,0))
# determines if there can still be a piece placed
def legal_check (board,selected_col):
    return board[5][selected_col] == 0
# identifies the row in which the piece lands
def where_it_lands (board,selected_col):
    for r in range(6):
        if board [r][selected_col] == 0:
            return r
#changes the entry in the matrice from 0 to either 1 or 2
def play (board, row, selected_col, piece):
    board[row][selected_col] = piece
# tells us if one of the Players won
def so_won (board,piece):
    for c in range(4):
        for r in range(6):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    for c in range(7):
        for r in range(3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    for c in range(4):
        for r in range(3):
            if board[r][c] == piece and board[r + 1][c+1] == piece and board[r + 2][c+2] == piece and board[r + 3][
                c+3] == piece:
                return True
    for c in range(4):
        for r in range(3,6):
            if board[r][c] == piece and board[r - 1][c+1] == piece and board[r - 2][c+2] == piece and board[r - 3][
                c+3] == piece:
                return True
# evaluetes moves based on how many pieces in a row you get
def value_function (board,piece):
    # nach welchen Kriterien soll bewertet werden?
    # Was bringt einem Speler einen Vorteil? - Anzahl an 2er- 3er-Reihen
    value=0
    for r in range (6):
        row_count=[int(i) for i in list(board[r,:])]
        for c in range(4):
            window=row_count[c:c+4]
            if window.count(piece) == 4:
                value += 100
            elif window.count(piece) == 3 and window.count(0)== 1:
                value += 30
            elif window.count(piece) == 2 and window.count(0)== 2:
                value += 10
    return value
# gives a list of all next possible moves
def all_legal_moves (board):
    legal_moves=[]
    for selected_col in range(7):
        if legal_check(board,selected_col):
            legal_moves.append(selected_col)
    return legal_moves
# function upon which the algorithm picks his move
def select_move(board,piece):
    legal_moves=all_legal_moves(board)
    best_value = 0
    best_col = random.choice(legal_moves)                         #elegantere Lösung???
    for selected_col in legal_moves:
        row=where_it_lands(board,selected_col)
        copied_board=board.copy()
        play(copied_board,row,selected_col,piece)
        value=value_function(copied_board,piece)
        if value > best_value:
            best_value=value
            best_col=selected_col
    return best_col


over=False
turn=0 # vielleicht Start ebenfalls zufällig generieren (mit random.randint(0,1))
while not over:

    if turn==0:
        selected_col= int(input("P1 choose (0-6):"))
        if legal_check(board,selected_col):
            row= where_it_lands(board,selected_col)
            play(board,row,selected_col,1)

            if so_won(board,1):
                print("P1 wins")
                over=True
# P2 ist jetzt "automatisiert": zufälliges Einsetzen
    else:

        #selected_col = random.randint(0,6)
        selected_col = select_move(board,piece=2)
        if legal_check(board,selected_col):
            row= where_it_lands(board,selected_col)
            play(board,row,selected_col,2)

            if so_won(board,2):
                print("P2 wins")
                over=True

    print_right_way(board)

    turn += 1
    turn = turn % 2




