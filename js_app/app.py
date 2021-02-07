from __future__ import print_function

import math
from flask import Flask, render_template, request

import os
import numpy as np
import webbrowser

from lib.players import AlphaBeta, MCTS

app = Flask(__name__)
# app.secret_key = 's3cr3t'
# app.debug = True
app._static_folder = os.path.abspath("templates/static/")
# host = '0.0.0.0'
# port = 5019
# url = 'http://' + host + ':' + str(port) + '/'
# webbrowser.open(url)


@app.route('/', methods=['GET'])
def index():
    return render_template('connect_html.html')


@app.route('/ai-action', methods=['GET', 'POST'])
def ai_action():
    """Get next action from the specified AI"""
    # POST request
    if request.method == 'POST':
        data = request.get_json(force=True)
        gameBoard = data['list'][0]
        ai = data['list'][1]
        x = call_AI(gameBoard, ai)

        return str(x), 200


def gameBoard_to_matrix(gameBoard):
    """Convert the JS gameBoard into a matrix to make it work with the AI implementation"""
    gameBoard = {int(k): v for k, v in gameBoard.items()}
    gameBoard = [list(v.values()) for v in gameBoard.values()]

    mapping = {'free': 0, 'red': 1, 'yellow': 2}
    gameBoard = [[mapping[x] for x in col] for col in gameBoard]

    gameBoardMatrix = np.array(gameBoard).T[:-2]

    return gameBoardMatrix


def call_AI(gameBoard, ai):
    """Call the specified AI"""
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


if __name__ == '__main__':
    app.run()
 