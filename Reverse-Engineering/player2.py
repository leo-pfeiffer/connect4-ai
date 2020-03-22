import board


class Player:
    maxPlayer = None
    minPlayer = None
    # list of moves and their weight
    last = []

    def __init__(self):
        # Each Player gets their own board
        self.b = board.Board()

    def name(self):
        return 'SKUNKOpp'

    def make_move(self, move):
        # Call make_move function of Board Class with parameters of Player 1
        self.b.make_move(move)

        # evaluation fuction : Maximizes the center of the board

    def evalfunc(self):
        #         count = 0
        #         lcount = 0
        #         fcount = 0
        #
        #         for x in range(0,5):
        #             for y in range(0,2):
        #                 if(self.b.state[(x,y)] == self.maxPlayer):
        #                     if(self.b.state[(x+1,y)] == self.maxPlayer and self.b.state[(x+1,y)] == self.maxPlayer):
        #                         lcount+=1
        #                     if(self.b.state[(x,y+1)] == self.maxPlayer and self.b.state[(x,y+2)] == self.maxPlayer):
        #                         lcount+=1
        #                     if(self.b.state[(x+1,y+1)] == self.maxPlayer and self.b.state[(x+2,y+2)] == self.maxPlayer):
        #                         lcount+=1
        #
        #         for i in range(0,6):
        #             if(self.b.state[(3,i)] == self.maxPlayer):
        #                 count+=1
        #         fcount = count*5
        #         count= 0
        #         for i in range(0,6):
        #             if(self.b.state[(2,i)] == self.maxPlayer):
        #                 count+=1
        #         fcount += count*3
        #         count= 0
        #         for i in range(0,6):
        #             if(self.b.state[(4,i)] == self.maxPlayer):
        #                 count+=1
        #         fcount += count*3
        #         count= 0
        #         for i in range(0,6):
        #             if(self.b.state[(5,i)] == self.maxPlayer):
        #                 count+=1
        #         fcount += count*2
        #         count= 0
        #         for i in range(0,6):
        #             if(self.b.state[(1,i)] == self.maxPlayer):
        #                 count+=1
        #         fcount += count*2

        return 100

    # alpha beta with pruning to find win
    def winner(self, depth, d, alpha, beta):

        if depth == 0:
            return self.evalfunc()

        if len(self.b.hist) != 0:
            if self.b.last_move_won() is True:
                if self.b.Player == self.maxPlayer:
                    return -10000
                else:
                    return 10000

        if self.b.Player == self.maxPlayer:
            value = alpha
            for i in self.b.generate_moves():
                self.b.make_move(i)
                # Winner func is called with depth -1 and new value
                # For MaxPlayer: value is max(previous value, new value)
                value = max(value, self.winner(depth - 1, d, alpha, beta))
                if value >= beta:
                    value = beta
                if depth == d:
                    self.last.append(value)

                # Pruning if not alpha <= value <= beta  (??)
                self.b.unmake_last_move()
            if depth == d:
                return self.last
            else:
                return value

        if self.b.Player == self.minPlayer:
            value = beta
            for i in self.b.generate_moves():
                self.b.make_move(i)
                # Just as before, only minimum of (previous value, new value)
                value = min(value, self.winner(depth - 1, d, alpha, beta))
                if value <= alpha:
                    value = alpha
                if depth == d:
                    self.last.append(value)
                self.b.unmake_last_move()
            if (depth == d):
                return self.last
            else:
                return value

    def get_move(self):
        # Define who is maximising and who is minimising player in this round
        self.maxPlayer = self.b.Player
        self.minPlayer = 3 - self.maxPlayer

        # Delete last moves (?)
        self.last.clear()

        self.winner(5, 5, -10000, 10000)
        #         else:
        #             self.winner(8, 8,-10000,10000)

        print(self.last)
        i = self.last.index(max(self.last))
        return self.b.generate_moves()[i]
