import datetime
import time
import pandas as pd
from lib.board import Board
from lib.players import Human, AlphaBeta, MCTS
from lib.gameplay import play_game


def reporter(players, num_sim, report_df):
    """
    Creates a report for output in a text file.
    Columns: No of game, Winner, No of cummulative wins, cummulative share of wins, runtime of game
    """

    h = "Game report"
    t = datetime.datetime.strftime(datetime.datetime.now(), format='%Y-%d-%m %H:%M:%S')
    o = players[0].name + " vs " + players[1].name
    g = "Number of games: " + str(num_sim)
    line_sep = "============================================\n"

    report_string = line_sep + h + "\n" + t + "\n" + o + "\n" + g + "\n" + line_sep + report_df.to_string()

    return report_string



def run_test(players, num_sim):

    report_df = pd.DataFrame(columns=['Winner', 'Cum_Wins', 'Cum_Wins_S', 'Runtime'], index=[*range(num_sim)])

    wins_p1 = 0
    wins_p2 = 0
    draws = 0

    for i in range(num_sim):
        start = time.time()

        board = Board.build_board()
        winner = play_game(players=players, board=board)

        runtime = time.time() - start

        if winner == players[0].name:
            wins_p1 += 1
            cum_wins = wins_p1
        if winner == players[1].name:
            wins_p2 += 1
            cum_wins = wins_p2
        if winner == 'DRAW':
            draws += 1
            cum_wins = draws

        cum_wins_p = cum_wins / (i + 1)

        report_df.iloc[i] = [winner, cum_wins, cum_wins_p, runtime]

    report_string = reporter(players, num_sim, report_df)
    print("Average runtime on {} runs: {}".format(num_sim, report_df.Runtime.mean()))

    timestamp = datetime.datetime.strftime(datetime.datetime.now(), format='%Y-%d-%m_%H:%M:%S')

    text_file = open("report_{}.txt".format(timestamp), "w")
    text_file.write(report_string)
    text_file.close()
    int(0)


if __name__ == '__main__':
    board = Board.build_board()

    H1 = Human(board, no=1, name='John Henry')
    H2 = Human(board, no=1, name='Elham')

    AB1 = AlphaBeta(board, no=2, name='Alphabeta1')
    AB2 = AlphaBeta(board, no=2, name='Alphabeta2')

    M1 = MCTS(board, no=1, name='MCTS1')
    M2 = MCTS(board, no=2, name='MCTS2')

    players = [M1, M2]

    run_test(players, num_sim=10)
    int(0)