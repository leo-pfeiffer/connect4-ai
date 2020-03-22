##Connect 4 player using A* and bit boards.

**This file is work in progress**

The following is an implementation of an AI connect 4 agent.

The repository contains the main code base and auxilary files used for testing.

1. board.py : This class contains the 2 boards for the two players implemented as a 64 bit binary. It also contains the transitions possible. And the functions to help with those transitions.
2. player.py: Contains the A* traversal algorithm. Contains the evaluation function for each state and also returns the moves.
3. player2.py and random_player.py: These were used to test against in development of the algorithm
4. search.py: Used to test the board integrity.
5. test.py: Used to test tree traversal.
6. test(1).py: Runs agents against each other. (Run this if you wanna see the magic!!)
