## Notice
This is the original version as it was developed for the uni project. 
For an updated version, check out the [V2](https://github.com/leo-pfeiffer/AI4Connect4/tree/v2)
branch. This updated version includes several code improvements and most importantly a Socket.io 
based multiplayer option for the web app.  

## Connect 4
The repository contains code for two AI implementations for the well-known
game Connect Four. Specifically, we've implemented both Alpha-Beta Pruning 
as well as Monte Carlo Tree Search and added a web app to play the game online.

###### 1. Code structure
The code is split into two folders, js_app and lib. The former contains all
the code necessary to build and run a JS web app for the game using flask.
The latter folder contains the actual code needed for the AI.<br />

1. js_app
    * /templates/static/script.js: JS logic for web app 
    * /templates/static/style.css: style sheet for wep app
    * /templates/connect_html.html: main html file
    * /app.py: Flask script to integrate python scripts in web app
    
2. lib
    * /board.py: Sets up the Board class (game board)
    * /gameplay.py: Runs the game locally without GUI (matrix representation)
    * /players.py: Sets up the player classes (AB, MCTS, Human). Includes the code for the AI.
    * /report.py: Reporting tool for testing.
    
   
###### 2. How to run the game
There are different ways to run the scripts and to play the game.
1. Play locally without GUI <br />
    Run the file gameplay.py and specify your players (see section 2.1). The game board is
    presented as a matrix and you can play by typing the desired column
    for your next move when asked for it.
2. Play locally with GUI <br />
    Run the file flasktest.py with your parameters set (see section 2.2). Your browser will open automatically and direct
    you to the specified localhost page. Follow the instructions on the screen.
3. Play online with GUI <br />
    We have published an online version of the game using pythonanwhere.com. 
    You can play online on https://leopfeiffer.pythonanywhere.com/

  
###### 2.1 Setting up your players in gameplay.py

When playing locally without GUI, you are required to specify your game settings manually.
Take a look at the snippet below, which can be found at the end of gameplay.py

```python
    H1 = Human(board, no=1, name='Leo')
    H2 = Human(board, no=2, name='Niko')

    AB1 = AlphaBeta(board, no=1, name='Alphabeta1', depth=1)
    AB2 = AlphaBeta(board, no=2, name='Alphabeta2', depth=3)

    M1 = MCTS(board, no=1, name='MCTS1')
    M2 = MCTS(board, no=2, name='MCTS2')

    players = [H1, AB2]
```

The ```players``` list specifies which players play against each other. 
In this case, Human 1 (```H1```) plays against Alpha Beta Pruning 2 (```H2```).
You can choose any combination of available players, however the first
player in the list must always be instantiated with the argument ```no=1``` and the
second player in the list with ```no=2```. For Alpha-Beta Pruning you can also set
the parameter ```depth``` to specify the search depth used by the AI. Note that 
deeper searches reduce performance. Generally speaking, winning against ```depth=4```
is already quite hard. Once you've set up the parameters, you can
run the file and play in the console. 

###### 2.2 Setting up your players in flasktest.py

To run the web app locally you need to set the parameters in flasktest.py first.
The host '0.0.0.0' is default, although it can be changed (you could e.g. use your IP address).
The port can be set arbitrarily. Make sure you use a port that's not used already.

```python
host = '0.0.0.0'
port = 5000
url = 'http://' + host + ':' + str(port) + '/'  # http://host:port/
webbrowser.open(url)
```
Once you've specified all this, you're good to go and can run the file. The web app
will open in your default browser automatically.
