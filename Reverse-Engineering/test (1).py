import time
import board
import player
import player2
import random_player
import search
import random


def test_Q1():
    print("TESTING FOR Q1")
    b = board.Board()
    init_str = str(b)

    # test move generator in initial position
    assert (b.generate_moves() == [0, 1, 2, 3, 4, 5, 6])

    # test last_move_won in initial position
    assert b.last_move_won() is False
    b.make_move(0)
    b.make_move(1)
    b.make_move(0)
    b.make_move(1)
    b.make_move(0)
    b.make_move(1)
    b.make_move(0)

    # test last_move_won in simple position
    assert b.last_move_won() is True
    b.unmake_last_move()
    b.unmake_last_move()
    b.unmake_last_move()
    b.unmake_last_move()
    b.unmake_last_move()
    b.unmake_last_move()
    b.unmake_last_move()

    # test the unmake operates correctly (assuming __str__() is correct)
    assert (init_str == str(b))

    # play 1000 random games to test make/unmake return board to start state
    for k in range(1000):
        i = 0
        while not b.last_move_won() and len(b.generate_moves()) > 0:
            moves = b.generate_moves()
            move = random.choice(moves)
            b.make_move(move)
            i += 1
        for j in range(i):
            b.unmake_last_move()
        assert (init_str == str(b))
    print("passed")


def test_Q2():
    print("TESTING FOR Q2")
    b = board.Board()
    assert (search.perft(b, 1) == 7)
    assert (search.perft(b, 8) == 5686266)
    b.make_move(0)
    b.make_move(2)
    b.make_move(0)
    assert (search.perft(b, 8) == 5245276)

    moves = [4, 3, 1, 2, 1, 4, 1, 4, 5, 6, 2, 2, 2, 0, 4, 1, 1, 0, 4, 6, 1, 0, 6, 5, 3, 5, 0, 3]
    perfts = [117649, 117648, 117431, 117430, 117213, 115461, 112707, 91787, 78679, 87247, 78383, 85599, 74934, 81279,
              66097, 73244, 86238, 73351, 74531, 56724, 56152, 21664, 18546, 13302, 13459, 9263, 4670, 4548]
    b = board.Board()
    for x in range(len(moves)):
        assert (search.perft(b, 6) == perfts[x])
        b.make_move(moves[x])
    print("passed")


def test_Q3():
    print("TESTING FOR Q3")
    b = board.Board()
    assert (search.find_win(b, 8) == "NO FORCED WIN IN 8 MOVES")
    b.make_move(2)
    b.make_move(0)
    b.make_move(3)
    b.make_move(0)
    assert (search.find_win(b, 3) == "WIN BY PLAYING 4")
    b.make_move(4)
    assert (search.find_win(b, 3) == "ALL MOVES LOSE")
    print("passed")


def test_Q4():
    players = [player.Player(), player2.Player()]
    random.shuffle(players)
    print(players[0].name() + " vs " + players[1].name())

    count = 0           # number of turns taken
    b = board.Board()   # initiate playing board
    i = 0               # index of current player: oscillates between 0 and 1
    legal_moves = b.generate_moves()    # list with all legal moves at start (i.e. selectable columns)

    while not b.last_move_won() and len(legal_moves) > 0:  # cond 1: Have winner; cond 2: Draw
        start_time = time.time()

        move = players[i].get_move()        # get move according to the algorithm the current player
        print("--- %s seconds ---" % (time.time() - start_time))
        print("MOVE: {}".format(move))

        players[0].make_move(move)          # save move to first player's board
        players[1].make_move(move)          # save move to second player's board
        b.make_move(move)                   # add current move to playing board
        count += 1
        print("COUNT: {}".format(count))
        i ^= 1                              # change player
        legal_moves = b.generate_moves()    # update legal moves

    if b.last_move_won():
        print("VICTORY FOR PLAYER " + players[i ^ 1].name())
    else:
        print("DRAW")


# test_Q1()
# test_Q2()
# test_Q3()
test_Q4()
