from __future__ import print_function

import math
from flask import Flask, render_template, request

import os
import numpy as np
import webbrowser

from lib.players import AlphaBeta, MCTS

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.debug = True
app._static_folder = os.path.abspath("templates/static/")
webbrowser.open('http://0.0.0.0:5011/')

@app.route('/', methods=['GET'])
def index():
    #title = 'Welcome to the Teisendorf-Challenge.\nCan you win against the AI?'
    return render_template('connect_html.html')


@app.route('/ai-action', methods=['GET', 'POST'])
def ai_action():

    # POST request
    if request.method == 'POST':
        data = request.get_json(force=True)
        gameBoard = data['list'][0]
        ai = data['list'][1]
        x = call_AI(gameBoard, ai)

        # return jsonify(x), 200
        return str(x), 200


def gameBoard_to_matrix(gameBoard):
    gameBoard = {int(k): v for k, v in gameBoard.items()}
    gameBoard = [list(v.values()) for v in gameBoard.values()]

    mapping = {'free': 0, 'red': 1, 'yellow': 2}
    gameBoard = [[mapping[x] for x in col] for col in gameBoard]

    gameBoardMatrix = np.array(gameBoard).T[:-2]

    return gameBoardMatrix


def call_AI(gameBoard, ai):
    board = gameBoard_to_matrix(gameBoard)
    if ai == 'AlphaBeta1':
        AB = AlphaBeta(board=board, no=2, name='AlphaBeta1', depth=1)
        selected_col = AB.selector(board, -math.inf, math.inf, True)
    elif ai == 'AlphaBeta2':
        AB = AlphaBeta(board=board, no=2, name='AlphaBeta2', depth=2)
        selected_col = AB.selector(board, -math.inf, math.inf, True)
    elif ai == 'AlphaBeta3':
        AB = AlphaBeta(board=board, no=2, name='AlphaBeta3', depth=3)
        selected_col = AB.selector(board, -math.inf, math.inf, True)
    elif ai == 'AlphaBeta4':
        AB = AlphaBeta(board=board, no=2, name='AlphaBeta3', depth=4)
        selected_col = AB.selector(board, -math.inf, math.inf, True)
    elif ai == 'AlphaBeta5':
        AB = AlphaBeta(board=board, no=2, name='AlphaBeta3', depth=5)
        selected_col = AB.selector(board, -math.inf, math.inf, True)
    elif ai == 'MCTS':
        M = MCTS(board=board, no=2, name='MCTS')
        selected_col = M.selector(board, -math.inf, math.inf, True)
    return selected_col


def matrix_to_gameBoard(gameBoardMatrix):
    """
    Not currently needed, but maybe later.
    """
    gameBoardMatrix = np.array(gameBoardMatrix).T
    gameBoard = [x + [0, 0] for x in gameBoardMatrix.tolist()]
    mapping = {0: 'free', 1: 'red', 2: 'yellow'}
    gameBoard = [[mapping[x] for x in col] for col in gameBoard]
    gameBoard = {str(k1): {str(k2): v2 for k2, v2 in zip(range(9), v1)} for k1, v1 in zip(range(7), gameBoard)}

    return gameBoard    # return this to GET request


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011)
