import numpy as np
import random

#build the foundations and get familiar with programme
# initialise board
def build_board():
    board=np.zeros((6,7))
    return board
board=build_board()
print(board)
# flip the board
def print_right_way (board):
    print(np.flip(board,0))
# checks if colums are legal to be played
def legal_check (board,selected_col):
    return board[5][selected_col] == 0
# gives the row where piece lands
def where_it_lands (board,selected_col):
    for r in range(6):
        if board [r][selected_col] == 0:
            return r
# changes matrix entry
def play (board, row, selected_col, piece):
    board[row][selected_col] = piece
# deterines if there is a winner
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
# returns a value of an action
def value_function (board, piece):
    score=0
    for r in range(6):
        row_array=[int(i) for i in list(board[r,:])]
        for c in range (4):
            window= row_array[c:c+4]
            if window.count(piece)==4:
                score +=100
            elif window.count(piece)==3 and window.count(0)== 1:
                score += 30
            elif window.count(piece)==2 and window.count(0)== 2:
                score += 10
    for c in range(7):
        col_array=[int(i) for i in list(board[:,c])]
        for r in range (3):
            window= col_array[r:r+4]
            if window.count(piece)==4:
                score +=100
            elif window.count(piece)==3 and window.count(0)== 1:
                score += 30
            elif window.count(piece)==2 and window.count(0)== 2:
                score += 10
    return score

def valid_locations (board):
    locations=[]
    for selected_col in range(7):
        if legal_check(board,selected_col):
            locations.append(selected_col)
    return locations

def AI_move (board,piece):
    locations=valid_locations(board)
    best_score=0
    col_move=random.choice(locations)
    for selected_col in locations:
        row= where_it_lands(board,selected_col)
        copied_board=board.copy()
        play(copied_board,row,selected_col,piece)
        score= value_function(copied_board,piece)
        if score> best_score:
            best_score= score
            col_move=selected_col
    return col_move

over=False
turn=0
while not over:

    if turn==0:
        selected_col= int(input("P1 choose (0-6):"))
        if legal_check(board,selected_col):
            row= where_it_lands(board,selected_col)
            play(board,row,selected_col,1)

            if so_won(board,1):
                print("P1 wins")
                over=True

    else:
        selected_col = AI_move(board,2)
        if legal_check(board,selected_col):
            row= where_it_lands(board,selected_col)
            play(board,row,selected_col,2)

            if so_won(board,2):
                print("P2 wins")
                over=True

    print_right_way(board)

    turn += 1
    turn = turn % 2




