class Board:
    """
    Creates a playing board for Connect-Four using bitboards.
    Each position on the board corresponds to an index in the bitboard (read from right to left),
    e.g. 0b0101101 describes the board with coins in positions 1, 3, 4 and 6

    Playing board:

       -----------------------------
    5:| 35, 36, 37, 38, 39, 40, 41, |
    4:| 28, 29, 30, 31, 32, 33, 34, |
    3:| 21, 22, 23, 24, 25, 26, 27, |
    2:| 14, 15, 16, 17, 18, 19, 20, |
    1:|  7,  8,  9, 10, 11, 12, 13, |
    0:|  0,  1,  2,  3,  4,  5,  6  |
       -----------------------------
         0,  1,  2,  3,  4,  5,  6

    """

    def __init__(self):
        self.myBoard = 0b0  # int(0)
        self.oppBoard = 0b0  # int(0)
        self.hist = []  # Records previous moves corresponding to the index of the respective position on the bitboard
        self.Player = 1

        # keys: columns, values: index of highest coin in column:
        # if any of the values > 41, we know that the column is full and hence not a legal move anymore
        self.available = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6}

        # Contains data for positive diagonal (/) check
        # Keys: base column of diagonal; values: number of moves upwards along the diagonal
        self.startposRange = {0: (0, 3), 1: (1, 3), 2: (2, 2), 3: (3, 1), 4: (4, 0), 5: (5, 0), 6: (14, 1), 7: (7, 2)}

        # Contains data for negative diagonal (\) check
        # Keys: base column of diagonal; values: number of moves downwards along the diagonal
        self.startnegRange = {0: (6, 3), 5: (5, 3), 4: (4, 2), 3: (3, 1), 2: (20, 1), 1: (13, 2)}

        self.testerpos = 0b1000000010000000100000001    # Pos 0-8-16-24
        self.testerneg = 0b1000001000001000001          # Pos 0-6-12-18

    def generate_moves(self):
        """
        Function excludes all columns from self.available that have value > 41. All others stay the same
        :return: list with all legal moves
        """
        moves = []
        for k in self.available:
            if self.available[k] <= 41:
                a = self.available[k] % 7
                moves.append(a)
        return moves

    def make_move(self, move):
        """Is called for both players and does the same thing dependent on the turn.
        Not sure what exactly it does. Somewhat updates the previous board with the current move"""

        # A mask covers portions of the bitfield that are not of interest (sets them to 0). What does it do here?
        mask = 0b1 << self.available[move]
        if self.Player == 1:  # if turn of Player 1
            self.myBoard = self.myBoard | mask  # | is bitwise OR operator
            self.Player = 3 - self.Player  # Switch player 1 <-> 2
        else:
            self.oppBoard = self.oppBoard | mask
            self.Player = 3 - self.Player
        self.hist.append(self.available[move])
        self.available[move] += 7  # one more coin in column 'move'

    def unmake_last_move(self):
        """
        Presumably called if connect4-pruning does not follow the move
        """

        maker = 0b1
        move = self.hist.pop()
        mask = maker << move

        if self.Player == 1:
            self.oppBoard = self.oppBoard ^ mask
        else:
            self.myBoard = self.myBoard ^ mask
        self.Player = 3 - self.Player
        self.available[move % 7] = self.available[move % 7] - 7  # one less coin in column 'move'

    def last_move_won(self):
        """
        Evaluate current bitboard to see wether we ahve arrived at a victory.
        This is the case if bitboard-shifting (twice) in a certain way leads to a bit value of 1.
        For more info visit section "Worked example" here:
        https://spin.atomicobject.com/2017/07/08/game-playing-ai-bitboards/

        :return: Boolean value, last move was win (True / False)
        """

        # get correct bitboard for current player
        if self.Player == 1:
            checkBoard = self.oppBoard
        else:
            checkBoard = self.myBoard

        # Check | (vertical)
        x = checkBoard & (checkBoard >> 7)
        if x & (x >> 2 * 7):
            return True

        """ # Why doesn't this work to check horizontal: Fails test2
        x = checkBoard & (checkBoard >> 1)
        if x & (x >> 2 * 1):
            return True
        """
        # Check - (horizontal)

        tester = 0b1111     # tester is active for elements 0, 1, 2, 3
        lastmove = 0
        if len(self.hist) > 0:          # only do if we're not in round one
            lastmove = self.hist[-1]    # get actual last move

        dist = lastmove - lastmove % 7  # lastmove % 7 gives column of last move; dist is first element of row.
        tester = tester << dist         # tester moves to row of last move and marks first 4 elements of row
        for i in range(0, 4):           # checks whether any 4 connected elements exist from left to right
            if (checkBoard & tester) == tester:
                return True
            else:
                tester = tester << 1    # moves tester one element to the right in the row of last move

        # Check / (positive diagonal)
        startpos = lastmove % 8                 # base element of /-diagional
        (x, y) = self.startposRange[startpos]   # x: base element of diagonal, y: number of moves along diagonal
        tester = self.testerpos << x            # moves tester to the diagonal to be checked

        for i in range(0, y):                   # check whether any 4 connected elements exist along the diagonal
            if (checkBoard & tester) == tester:
                return True
            else:
                tester = tester << 8             # moves tester one element upwards along the diagonal

        # Check \ (negative diagonal)
        startpos = lastmove % 6                 # base element of \-diagonal
        (x, y) = self.startnegRange[startpos]   # x: base element of diagonal, y: number of moves along diagonal
        tester = self.testerneg << x            # moves tester to the diagonal to be checked

        for i in range(0, y):                   # check whether any 4 connected elements exist along the diagonal
            if (checkBoard & tester) == tester:
                return True
            else:
                tester = tester << 6            # Probably: moves test-diagonal one row upwards

        return False

    def __str__(self):
        a = "{0:b}".format(self.myBoard)
        b = "{0:b}".format(self.oppBoard)
        return "MaxPlayer: " + a + " MinPLayer: " + b
