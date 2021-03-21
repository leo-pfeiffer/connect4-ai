import random
import string


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


def get_game_by_id(games, game_id):
    if len(games) == 0:
        return None
    matchingGames = [g for g in games if g.game_id == game_id]
    if len(matchingGames) == 0:
        return None
    return matchingGames[0]


def games_of_player(games, sid: str):
    return [g for g in games if len([p for p in g.players if p.sid == sid]) > 0]


def remove_game(games, game):
    return [g for g in games if g.game_id != game.game_id]

