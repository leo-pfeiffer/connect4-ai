import board
import time

last = []


def doperft(b, depth):
    NodeCount = 0

    for i in b.generate_moves():
        b.make_move(i)
        if depth == 0:
            NodeCount += 1
        elif b.last_move_won():
            NodeCount += 1
        else:
            NodeCount += doperft(b, depth - 1)
        b.unmake_last_move()
    return NodeCount


def perft(b, depth):
    return doperft(b, depth - 1)


def test(b):
    vertCheck = 0b100000010000001
    posCheck = 0b10000000100000001
    negCheck = 0b1000001000001
    count = 0
    testB = b.myBoard
    for i in range(0, 14):
        if (testB & (vertCheck << i)) == (vertCheck << i):
            count += 1
        if (testB & (posCheck << i)) == (posCheck << i):
            count += 1
        if (testB & (negCheck << i)) == (negCheck << i):
            count += 1
    return count


def evaluate(b, minPlayer, maxPlayer):
    if b.last_move_won():
        if b.Player == maxPlayer:
            return -1
        else:
            return 1
    else:
        return 0


# alpha beta to find win
def winner(b, depth, d, alpha, beta, minPlayer, maxPlayer):
    # leaf node
    if depth == 0:
        return evaluate(b, minPlayer, maxPlayer)

    # win leaf node
    if len(b.hist) != 0:
        if b.last_move_won() == True:
            return evaluate(b, minPlayer, maxPlayer)

    # maximiser
    if b.Player == maxPlayer:
        value = alpha
        for i in b.generate_moves():
            b.make_move(i)
            value = max(value, winner(b, depth - 1, d, alpha, beta, minPlayer, maxPlayer))
            if value >= beta:
                b.unmake_last_move()
                return beta
            if depth == d:
                last.append(value)
            b.unmake_last_move()
        if depth == d:
            return [max(last), last.index(max(last))]
        else:
            return value

    # minimiser
    if b.Player == minPlayer:
        value = beta
        for i in b.generate_moves():
            b.make_move(i)
            value = min(value, winner(b, depth - 1, d, alpha, beta, minPlayer, maxPlayer))
            if value <= alpha:
                b.unmake_last_move()
                return alpha
            b.unmake_last_move()
        return value


def find_win(b, depth):
    maxPlayer = b.Player
    minPlayer = 3 - maxPlayer
    result = winner(b, depth, depth, -10, 10, minPlayer, maxPlayer)
    last.clear()

    # return results
    if (result[0] == 0):
        return "NO FORCED WIN IN " + str(depth) + " MOVES"
    elif (result[0] == 1):
        return "WIN BY PLAYING " + str(result[1])
    elif (result[0] == -1):
        return "ALL MOVES LOSE"
