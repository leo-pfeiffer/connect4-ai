import numpy as np
import random

#build the foundations and get familiar with programme
# initialise board
def build_board():
    board=np.zeros((6,7))
    return board
board=build_board()
print(board)

def print_right_way (board):
    print(np.flip(board,0))

def legal_check (board,selected_col):
    return board[5][selected_col] == 0

def where_it_lands (board,selected_col):
    for r in range(6):
        if board [r][selected_col] == 0:
            return r
def play (board, row, selected_col, piece):
    board[row][selected_col] = piece

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

def value_function (board,piece):
    # nach welchen Kriterien soll bewertet werden?
    # Was bringt einem Speler einen Vorteil? - Anzahl an 2er- 3er-Reihen


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
        selected_col = random.randint(0,6)
        if legal_check(board,selected_col):
            row= where_it_lands(board,selected_col)
            play(board,row,selected_col,2)

            if so_won(board,2):
                print("P2 wins")
                over=True

    print_right_way(board)

    turn += 1
    turn = turn % 2




