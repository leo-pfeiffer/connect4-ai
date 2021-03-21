from __future__ import print_function

import math
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room

import os
import numpy as np
import string
import random

from lib.players import AlphaBeta, MCTS


# Keep track of open Games
class Game:
    def __init__(self):
        # random ID
        self._game_id = ''.join(random.choice(string.ascii_uppercase) for i in range(2))
        self._players = set()

    @property
    def game_id(self):
        return self._game_id

    @property
    def players(self):
        return self._players

    def add_player(self, player):
        assert len(self.players) < 2
        self._players.add(player)

    def remove_player(self, player):
        self._players.remove(player)

    def get_player_by_sid(self, sid):
        if len(self.players) == 0:
            return None
        matchingPlayers = [p for p in self.players if p.sid == sid]
        if len(matchingPlayers) == 0:
            return None
        return matchingPlayers[0]


# Players
class Player:
    def __init__(self, sid):
        self._sid = sid

    @property
    def sid(self):
        return self._sid

#
# # Active games
# games = []
#
#
# def get_game_by_id(id):
#     if len(games) == 0:
#         return None
#     matchingGames = [g for g in games if g.game_id == id]
#     if len(matchingGames) == 0:
#         return None
#     return matchingGames[0]
#
#
# def games_of_player(sid: str):
#     return [g for g in games if len([p for p in g.players if p.sid == sid]) > 0]
#
#
# def remove_game(game):
#     return [g for g in games if g.game_id != game.game_id]


# Flask
app = Flask(__name__)
app._static_folder = os.path.abspath("templates/static/")

socketio = SocketIO(app)

#
# # SocketIO === START ===
#
# @socketio.on('json')
# def handle_json(json):
#     print('received json: ' + str(json))
#     send(json, json=True)
#
#
# @socketio.on('message')
# def handle_message(data):
#     print('received message: ' + data)
#     send(data)
#
#
# @socketio.on('ping')
# def handle_ping(data):
#     print('ping: ' + data['data'])
#     emit('ping', 'pong')
#
#
# @socketio.on('disconnect')
# def handle_disconnect():
#
#     text = f"Player {request.sid} disconnected. Game was closed."
#     print(text)
#
#     games_to_remove = games_of_player(request.sid)
#     for game in games_to_remove:
#         remove_game(game)
#         emit('disconnect-info', {'text': text}, room=game.game_id)
#
# # SocketIO === END ===
#

@app.route('/', methods=['GET'])
def index():
    return render_template('connect_html.html')

#
# @app.route('/ai-action', methods=['GET', 'POST'])
# def ai_action():
#     """Get next action from the specified AI"""
#     # POST request
#     if request.method == 'POST':
#         data = request.get_json(force=True)
#         gameBoard = data['list'][0]
#         ai = data['list'][1]
#         x = call_AI(gameBoard, ai)
#
#         return str(x), 200
#
#
# @socketio.on('ai-action')
# def on_ai_action(data):
#     gameBoard = data['gameBoard']
#     ai = data['opponent']
#     x = call_AI(gameBoard, ai)
#
#     emit('ai-action', str(x))
#
#
# @socketio.on('user-action')
# def on_user_action(data):
#
#     game_id = data['gameId']
#     assert game_id is not None
#     game = get_game_by_id(game_id)
#     assert game is not None
#
#     response_data = {
#         'text': request.sid + ' played column ' + str(data['col']),
#         'col': data['col'],
#         'game': game.game_id,
#         'player': data['player']
#     }
#
#     emit('user-action', response_data, room=game_id)
#
#
# @socketio.on('create')
# def on_create():
#
#     player = Player(request.sid)
#     game = Game()
#     game.add_player(player)
#
#     games.append(game)
#
#     room = game.game_id
#     join_room(room)
#
#     print('Created: ' + room)
#
#     response_data = {
#         'text': request.sid + ' has entered game ' + game.game_id,
#         'game': game.game_id
#     }
#
#     emit('create', response_data, room=room)
#
#
# @socketio.on('join')
# def on_join(data):
#     room = data['game']
#
#     # Make sure game exists and is not duplicate
#     matchingGames = [g for g in games if g.game_id == room]
#     assert len(matchingGames) == 1
#
#     player = Player(request.sid)
#     matchingGames[0].add_player(player)
#
#     join_room(room)
#
#     response_data = {
#         'text': request.sid + ' has entered game ' + room,
#         'game': room
#     }
#
#     emit('join', response_data, room=room)
#
#
# @socketio.on('leave')
# def on_leave(data):
#     room = data['game']
#
#     matchingGames = [g for g in games if g.game_id == room]
#     assert len(matchingGames) == 1
#
#     game = matchingGames[0]
#     matchingPlayers = [p for p in game.players if p.sid == request.sid]
#     assert len(matchingPlayers) == 1
#
#     player = matchingPlayers[0]
#     game.remove_player(player)
#
#     leave_room(room)
#
#     send(request.sid + ' has left the room.', room=room)
#
#
# def gameBoard_to_matrix(gameBoard):
#     """Convert the JS gameBoard into a matrix to make it work with the AI implementation"""
#     gameBoard = {int(k): v for k, v in gameBoard.items()}
#     gameBoard = [list(v.values()) for v in gameBoard.values()]
#
#     mapping = {'free': 0, 'red': 1, 'yellow': 2}
#     gameBoard = [[mapping[x] for x in col] for col in gameBoard]
#
#     gameBoardMatrix = np.array(gameBoard).T[:-2]
#
#     return gameBoardMatrix
#
#
# def call_AI(gameBoard, ai):
#     """Call the specified AI"""
#     board = gameBoard_to_matrix(gameBoard)
#     if ai == 'AlphaBeta1':
#         AB = AlphaBeta(board=board, no=2, name='AlphaBeta1', depth=1)
#         selected_col = AB.selector(board, -math.inf, math.inf, True)
#     elif ai == 'AlphaBeta2':
#         AB = AlphaBeta(board=board, no=2, name='AlphaBeta2', depth=2)
#         selected_col = AB.selector(board, -math.inf, math.inf, True)
#     elif ai == 'AlphaBeta3':
#         AB = AlphaBeta(board=board, no=2, name='AlphaBeta3', depth=3)
#         selected_col = AB.selector(board, -math.inf, math.inf, True)
#     elif ai == 'AlphaBeta4':
#         AB = AlphaBeta(board=board, no=2, name='AlphaBeta3', depth=4)
#         selected_col = AB.selector(board, -math.inf, math.inf, True)
#     elif ai == 'AlphaBeta5':
#         AB = AlphaBeta(board=board, no=2, name='AlphaBeta3', depth=5)
#         selected_col = AB.selector(board, -math.inf, math.inf, True)
#     elif ai == 'MCTS':
#         M = MCTS(board=board, no=2, name='MCTS')
#         selected_col = M.selector(board, -math.inf, math.inf, True)
#     return selected_col


if __name__ == '__main__':
    # app.run()
    socketio.run(app)
