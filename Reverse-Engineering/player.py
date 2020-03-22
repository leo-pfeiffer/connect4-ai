import board
import time
import operator


class Player:
    maxPlayer = None
    minPlayer = None
    colChecker = 0b100000010000001000000100000010000001
    # list of moves and their weight
    last = []
    startTime = 0
    outtaTime = False

    def __init__(self):
        # Each player gets their own board
        self.b = board.Board()

    def name(self):
        return 'SKUNK'

    def make_move(self, move):
        # Call the male_move function of the board class with parameters of Player 1
        self.b.make_move(move)

        # evaluation fuction : Maximizes the center of the board

    def evalfunc(self):

        if self.maxPlayer == 1:
            testB = self.b.myBoard
            testQ = self.b.oppBoard
            add = 200
            sub = 100
        else:
            testB = self.b.oppBoard
            testQ = self.b.myBoard
            add = 200
            sub = 100

        count = 0
        minCount = 0

        vertCheck = 0b100000010000001
        empty = 0b1
        posCheck = 0b10000000100000001
        negCheck = 0b1000001000001
        for i in range(7, 21):
            if (testB & (vertCheck << i)) == (vertCheck << i) and (testQ & (empty << i + 28) == 0):
                count += add
            if (testB & (posCheck << i)) == (posCheck << i) and (testQ & (empty << i) == 0):
                count += add
            if (testB & (negCheck << i)) == (negCheck << i) and (testQ & (empty << i) == 0):
                count += add

        for i in range(0, 14):
            if (testQ & (vertCheck << i)) == (vertCheck << i) and (testB & (empty << i + 28) == 0):
                minCount += sub
            if (testQ & (posCheck << i)) == (posCheck << i) and (testB & (empty << i) == 0):
                minCount += sub
            if (testQ & (negCheck << i)) == (negCheck << i) and (testB & (empty << i) == 0):
                minCount += sub

        if self.maxPlayer == 1:
            fcount = count
        else:
            fcount = count - minCount
        fcount += 100 * bin(testB & (self.colChecker << 3)).count('1')
        fcount += 70 * bin(testB & (self.colChecker << 4)).count('1')
        fcount += 50 * bin(testB & (self.colChecker << 1)).count('1')
        fcount += 70 * bin(testB & (self.colChecker << 2)).count('1')
        fcount += 50 * bin(testB & (self.colChecker << 5)).count('1')

        return fcount

    # alpha beta with pruning to find win
    def winner(self, depth, d, alpha, beta, moveOrder):

        if time.time() - self.startTime > 2.87:
            self.outtaTime = True
            return 0

        if depth == 0:
            return self.evalfunc()

        if len(self.b.hist) + depth > 7:
            if self.b.last_move_won() is True:
                if self.b.Player == self.maxPlayer:
                    return -10000
                else:
                    return 10000

        if self.b.Player == self.maxPlayer:
            value = alpha
            for i in moveOrder:
                self.b.make_move(i)
                value = max(value, self.winner(depth - 1, d, alpha, beta, self.b.generate_moves()))
                if value >= beta:
                    value = beta
                if depth == d:
                    self.last.append(value)

                self.b.unmake_last_move()
            if depth == d:
                return self.last
            else:
                return value

        if self.b.Player == self.minPlayer:
            value = beta
            for i in self.b.generate_moves():
                self.b.make_move(i)
                value = min(value, self.winner(depth - 1, d, alpha, beta, self.b.generate_moves()))
                if value <= alpha:
                    value = alpha
                if depth == d:
                    self.last.append(value)
                self.b.unmake_last_move()
            if depth == d:
                return self.last
            else:
                return value

    def get_move(self):
        # Define who is maximising and who is minimising player in this round
        self.maxPlayer = self.b.Player
        self.minPlayer = 3 - self.maxPlayer

        self.outtaTime = False
        self.startTime = time.time()

        temp = []
        order = [1]
        number = 2

        # legal moves
        avail = self.b.generate_moves()
        moveOrder = {}

        for i in avail:
            if i == 3:
                moveOrder[i] = 1
            else:
                moveOrder[i] = 0

        while self.outtaTime is False:  # self.outtaTime defined during self.winner()
            temp.clear()
            temp.extend(self.last)

            if number > 2:
                j = 0
                for i in order:
                    if j == 0:  # first iteration
                        moveOrder[i] = temp[j]
                    elif temp[j] == temp[j - 1]:
                        moveOrder[i] = 0
                    else:
                        moveOrder[i] = temp[j]
                    j += 1
            order.clear()

            for i in sorted(moveOrder.items(), key=operator.itemgetter(1), reverse=True):
                (x, y) = i
                order.append(x)
            self.last.clear()
            self.winner(number, number, -10000, 10000, order)
            number += 1


        i = temp.index(max(temp))
        (move, weight) = sorted(moveOrder.items(), key=operator.itemgetter(1), reverse=True)[0]

        return move
