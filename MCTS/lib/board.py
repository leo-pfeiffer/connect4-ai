"""
File sets up the 6x7 playing board for Connect4
"""


class Board:

    def __init__(self):
        self.myBoard = 0b0
        self.oppBoard = 0b0
        self.hist = []
        self.Player = 1

        # keys: (?), values: available columns
        self.available = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6};

        self.startposRange = {0: (0, 3), 1: (1, 3), 2: (2, 2), 3: (3, 1), 4: (4, 0), 5: (5, 0), 6: (14, 1), 7: (7, 2)}

        self.startnegRange = {0: (6, 3), 5: (5, 3), 4: (4, 2), 3: (3, 1), 2: (20, 1), 1: (13, 2)}

        self.testerpos = 0b1000000010000000100000001
        self.testerneg = 0b1000001000001000001

    def generate_moves(self):
        moves = []
        for k in self.available:
            if self.available[k] <= 41:
                a = self.available[k] % 7
                moves.append(a)
        return moves

    def make_move(self, move):

        mask = 0b1 << self.available[move]
        if (self.Player == 1):
            self.myBoard = self.myBoard | mask
            self.Player = 3 - self.Player
        else:
            self.oppBoard = self.oppBoard | mask
            self.Player = 3 - self.Player
        self.hist.append(self.available[move])
        self.available[move] += 7

    def unmake_last_move(self):
        maker = 0b1
        move = self.hist.pop()
        mask = maker << move

        if self.Player == 1:
            self.oppBoard = self.oppBoard ^ mask
        else:
            self.myBoard = self.myBoard ^ mask
        self.Player = 3 - self.Player
        self.available[move % 7] = self.available[move % 7] - 7

    def last_move_won(self):
        if self.Player == 1:
            checkBoard = self.oppBoard
        else:
            checkBoard = self.myBoard
        #       Vertical
        x = checkBoard & (checkBoard << 7)
        if x & (x << 14):
            return True
        # Hor
        tester = 0b1111
        # make it global...
        lastmove = 0
        if (len(self.hist) > 0):
            lastmove = self.hist[-1]
        dist = lastmove - lastmove % 7
        tester = tester << dist
        for i in range(0, 4):
            if ((checkBoard & tester) == tester):
                return True
            else:
                tester = tester << 1

        # POS
        startpos = lastmove % 8
        (x, y) = self.startposRange[startpos]

        test = self.testerpos << x

        for i in range(0, y):
            if (checkBoard & test) == test:
                return True
            else:
                test = test << 8
        #
        #         Neg
        startpos = lastmove % 6
        (x, y) = self.startnegRange[startpos]
        test = self.testerneg << x

        for i in range(0, y):
            if (checkBoard & test) == test:
                return True
            else:
                test = test << 6

        return False

    def __str__(self):
        a = "{0:b}".format(self.myBoard)
        b = "{0:b}".format(self.oppBoard)
        return "MaxPlayer: " + a + " MinPLayer: " + b
