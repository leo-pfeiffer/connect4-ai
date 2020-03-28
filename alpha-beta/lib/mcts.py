import math
import numpy as np
from lib.main import build_board, legal_check, where_it_lands, play, so_won, print_right_way, minimax, valid_locations, \
    terminal_node


class MCTS:

    def __init__(self, board):
        self.board = board
        self.values = np.zeros((6, 7))
        self.total_visits = np.zeros((6, 7), dtype=int)
        self.cur_visits = np.zeros((6, 7), dtype=int)  # reset during every new selection.
        self.involved_nodes = []

    def selection(self, board):
        self.board = board

        self.current_visits = np.zeros((6, 7), dtype=int)  # n_j

        legal_cols = valid_locations(board)
        leg_mov_rows = self.legal_cols_row(self.board, legal_cols)
        legal_positions = [(r, c) for r, c in zip(leg_mov_rows, legal_cols)]

        # get UCT values for all legal_positions
        uct_values = [self.uct_value(self.values[x[0][1]], self.total_visits, self.cur_visits) for x in legal_positions]

        # select move with maximum uct value
        select = legal_positions[np.argmax(uct_values)]

        self.expansion(root=select)

        # now that we have an updated value matrix, select most promising action
        leg_mov_values = [self.values[x[0]][x[1]] for x in legal_positions]
        best_move = legal_cols[np.argmax[leg_mov_values]]

        return best_move

    def expansion(self, child):
        if terminal_node(child):
            self.total_visits[child[0]][child[1]] += 1
            n = self.total_visits[child[0]][child[1]]
            if so_won(board, 2):  # AI won
                self.values[child[0]][child[1]] = (self.values[child[0]][child[1]] * (n - 1) + 1) / n
                return 1
            elif so_won(board, 1):  # Human won
                self.values[child[0]][child[1]] = (self.values[child[0]][child[1]] * (n - 1)) / n
            else:  # Draw
                self.values[child[0]][child[1]] = (self.values[child[0]][child[1]] * (n - 1) + 0.5) / n
        else:
            self.simulation(self, child)

    def simulation(self, child):
        # Launch MC-simulation from child node.
        # Assume uniform random moves
        # In each iteration update the self.cur_visits and do self.total_visits[select_pos[0]][select_pos[1]] += 1
        # add every node that was played as a tuple to self.involved_nodes
        # when end of game is reached or time_out: call backpropagation
        pass

    def backpropagation(self):
        # Evaluate win/loss/draw
        # Update values for all nodes in self.involved_nodes using self.cur_visits
        pass

    @staticmethod
    def uct_value(x, total_n, current_n):
        if current_n == 0:  # force exploration of unvisited nodes
            return np.inf
        else:
            c = 1 / math.sqrt(2)  # fulfils Hoeffding-Inequality :P
            return x + 2 * c * math.sqrt((2 * math.log(total_n)) / current_n)

    @staticmethod
    def legal_cols_row(board, legal_cols):
        lcr = []
        for r in range(5, -1, -1):
            for c in legal_cols:
                if board[r][c] == 0:
                    lcr.append(r)
        return lcr


if __name__ == '__main__':

    board = build_board()
    print(board)

    over = False
    turn = 0

    M = MCTS(board)

    while not over:

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
            # get the best move
            selected_col = M.selection(board=board)
            # selected_col, minimax_score = minimax(board, 3, -math.inf, math.inf, True)
            if legal_check(board, selected_col):
                row = where_it_lands(board, selected_col)
                play(board, row, selected_col, 2)

                if so_won(board, 2):
                    print("AI wins")
                    over = True

        print_right_way(board)

        turn += 1
        turn = turn % 2
