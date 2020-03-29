import math
import numpy as np
import random
import time
from lib.main import Board


class MCTS:

    def __init__(self, board, no):
        self.board = board
        self.no = no    # Is MCTS Player 1 or Player 2
        self.values = np.zeros((6, 7))
        self.N = 0  # number of visits from child node = # of turns per simulation
        self.cur_visits = np.zeros((6, 7), dtype=int)  # reset during every new selection.
        self.involved_nodes = []

    def selection(self, board):
        self.board = board
        self.cur_visits = np.zeros((6, 7), dtype=int)  # n_j

        legal_cols = Board.valid_locations(board)
        leg_mov_rows = self.legal_cols_row(self.board, legal_cols)
        legal_pos = [(r, c) for r, c in zip(leg_mov_rows, legal_cols)]

        # get UCT values for all legal_positions
        uct_values = [self.uct_value(self.values[x[0]][x[1]], self.N, self.cur_visits[x[0]][x[1]]) for x in legal_pos]

        # select move with maximum uct value
        select = legal_pos[np.argmax(uct_values)]

        self.expansion(child=select)

        # now that we have an updated value matrix, select most promising action
        leg_mov_values = [self.values[x[0]][x[1]] for x in legal_pos]
        best_move = legal_cols[np.argmax(leg_mov_values)]

        return best_move

    def expansion(self, child):
        temp_board = self.board.copy()
        Board.play(temp_board, child[0], child[1], self.no)
        if Board.terminal_node(temp_board):
            self.N += 1
            if Board.so_won(self.board, self.no):  # MCTS won
                self.values[child[0]][child[1]] = (self.values[child[0]][child[1]] * (self.N - 1) + 1) / self.N
                return 1
            elif Board.so_won(self.board, 3 - self.no):  # Opponent won
                self.values[child[0]][child[1]] = (self.values[child[0]][child[1]] * (self.N - 1)) / self.N
            else:  # Draw
                self.values[child[0]][child[1]] = (self.values[child[0]][child[1]] * (self.N - 1) + 0.5) / self.N
        else:
            self.simulation(child)

    def simulation(self, child):
        print("AI is thinking... give it a second.\n============")
        startTime = time.time()
        outtaTime = False

        while not outtaTime:
            simu_board = self.board.copy()
            Board.play(simu_board, child[0], child[1], self.no)

            over = False
            turn = 0

            while not over:

                # Turn changes from 0 to 1 in each iteration. AI = 1, Human = 0.
                # Human behaves very stupid and chooses randomly.
                try:
                    selected_col = random.choice(Board.valid_locations(simu_board))
                # if no valid_locations left but no winner => DRAW. Backpropagate 0.5
                except IndexError:
                    self.backpropagation(result=0.5)
                    break
                row = Board.where_it_lands(simu_board, selected_col)

                if turn == 1:
                    self.cur_visits[row][selected_col] += 1         # update n of simulated nodes
                    self.N += 1      # update N of child_node
                    self.involved_nodes.append((row, selected_col))

                Board.play(simu_board, row, selected_col, turn + 1)

                if Board.so_won(simu_board, turn + 1):
                    # backpropagate result from perspective of AI: 1 if win, 0 if loss
                    self.backpropagation(result=turn)
                    over = True

                turn ^= 1

            playTime = time.time() - startTime
            outtaTime = (playTime > 3)      # stop simulating after 3 seconds

    def backpropagation(self, result):
        for node in self.involved_nodes:
            self.values[node[0]][node[1]] = (self.values[node[0]][node[1]] * (self.N - 1) + result) / self.N

        self.involved_nodes.clear()
        self.cur_visits = np.zeros((6, 7), dtype=int)
        self.N = 0

    @staticmethod
    def uct_value(x, N, n):
        if n == 0:  # force exploration of unvisited nodes
            return np.inf
        else:
            c = 1 / math.sqrt(2)  # fulfils Hoeffding-Inequality :P
            return x + 2 * c * math.sqrt((2 * math.log(N)) / n)

    @staticmethod
    def legal_cols_row(board, legal_cols):
        lcr = []
        for r in range(5, -1, -1):
            for c in legal_cols:
                if board[r][c] == 0:
                    lcr.append(r)
        return lcr


if __name__ == '__main__':

    board = Board.build_board()
    print(board)
    print("============\n")

    over = False
    turn = 0

    M = MCTS(board, no=2)

    while not over:

        # Human
        if turn == 0:
            selected_col = int(input("P1 choose (0-6):"))
            if Board.legal_check(board, selected_col):
                row = Board.where_it_lands(board, selected_col)
                Board.play(board, row, selected_col, 1)

                if Board.so_won(board, 1):
                    print("Human wins. Congratulations, John Henry.")
                    over = True
            # If illegal column is selected, ask the user again. => Outsourcing in function necessary
            else:
                print("Selected illegal column. Idiot! Your intelligence is artificial. GAME OVER!")
                break

        # AI
        else:
            # get the best move
            selected_col = M.selection(board=board)
            row = Board.where_it_lands(board, selected_col)
            Board.play(board, row, selected_col, 2)

            if Board.so_won(board, 2):
                print("AI wins. Death to humanity!")
                over = True

        Board.print_right_way(board)
        print("============\n")

        turn ^= 1
