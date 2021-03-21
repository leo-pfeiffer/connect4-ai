window.onload = function() {
    makeGame();
    // makeGame();

    // Modal
    const modal = document.getElementById('settings-modal')
	document.getElementById('open-settings-modal').onclick = () => {modal.classList.add('is-active')}
	document.getElementById('close-settings-modal').onclick = () => {modal.classList.remove('is-active')}
}

const makeGame = function() {

	// SocketIO socket
	const socket = io();

	// process ai-action response
	socket.on('ai-action', col => {
		console.log('Socket: AI played column ' + col);
		markNextFree(col)
	});

	const delimiters = ["[[", "]]"];

	let game = Vue.observable({
		state: "entry",
		gameId: null,
		mode: null,
	})

	let gameBoard = {};
	let currentPlayer = 'red';
	const numRows = 6;
	const numCols = 7;
	let numTurns = 0;
	let opponent = "None";

	const setState = function(newState) {
		game.state = newState;
	}

	const setMultiPlayerMode = function() {
		game.mode = 'multi';
	}

	const setSinglePlayerMode = function() {
		game.mode = 'single';
	}

	const setupGameBoard = function () {
		// initiate gameBoard with all positions free
		for (let x = 0; x <= numRows; x++) {
			gameBoard[x] = {};
			for (let y = 0; y <= numCols; y++) {
				gameBoard[x][y] = 'free';
			}
		}
	};

	const markNextFree = function (x) {
		// x: x-value of clicked column
		// get the next free position in the column or alert that column is full

		if (opponent === "None"){
			alert("To start the game, select your opponent and click submit.")
			return;
		}

		let nextY;
		nextY = false;

		for (let y = 0; y < numRows; y++) {
			if (gameBoard[x][y] === 'free') {
				nextY = y;
				break;
			}
		}

		// column full
		if (nextY === false) {
			console.log('full column ' + x)
			return false;
		}

		// mark free position with piece of current player
		gameBoard[x][nextY] = currentPlayer;

		// todo VUE
		// set the attribute of the played position to currentPlayer ('red' or 'yellow')
		document.querySelector('#column-' + x + ' .row-' + nextY + ' circle').setAttribute(
			'class', currentPlayer
		);

		// check if game is over
		if (isWinner(parseInt(x), nextY)) {
			alert(currentPlayer + ' wins!');
			console.log(currentPlayer + ' wins!');
			clearBoard();
			return true;
		}

		numTurns++;

		if (numTurns >= numRows * numCols) {
			alert('DRAW!');
			console.log('DRAW!');
			clearBoard();
			return true;
		}

		// change player color
		currentPlayer = currentPlayer === 'red' ? 'yellow' : 'red';

		// automatically get next move from AI unless opponent == human
		if (currentPlayer === 'yellow' && opponent !== 'Human'){
			getMoveFromAI()
		}

	};
	const clearBoard = function () {

		// todo VUE
		// reset attributes
		Array.prototype.forEach.call(document.querySelectorAll('circle'), function (piece) {
			piece.setAttribute('class', 'empty');
		});

		// reset gameBoard
		setupGameBoard();

		// reset variables
		numTurns = 0;
		currentPlayer = 'red';

		return gameBoard;
	};

	// check whether a coordinate is on the board
	const onBoard = function (x, y) {
		return (gameBoard.hasOwnProperty(x) && typeof gameBoard[x][y] !== 'undefined');

	};

	const getMoveFromAI = function () {

		if (opponent === 'Human') return

		// Emit action to socket
		socket.emit('ai-action', {
			gameBoard: gameBoard,
			opponent: opponent
		})

		// // POST
		// fetch('/ai-action', {
		// 	method: 'POST',
		// 	body: JSON.stringify({ 'list': [gameBoard, opponent]})
		// }).then(function (response) {
		// 	return response.text();
		// }).then(function (col) {
		// 	console.log('POST: AI played column ' + col);
		// 	return col;
		// }).then(markNextFree);
	};

	// check whether there are four connected pieces
	const checkDirection = function (currentX, currentY, direction) {

		// chainLength gives largest number of connected elements from current piece
		let chainLength, directions;

		// move according to the specified array: [[x1, y1], [x2, y2], ...]
		directions = {
			horizontal: [[0, -1], [0, 1]],
			vertical: [[-1, 0], [1, 0]],
			diagonal_up: [[-1, -1], [1, 1]],
			diagonal_down: [[-1, 1], [1, -1]],
		};

		chainLength = 1;

		directions[direction].forEach(function (coords) {

			let i = 1;
			// Search chain: chain on board && only currentPlayer
			while (onBoard(currentX + (coords[0] * i), currentY + (coords[1] * i)) &&
				(gameBoard[currentX + (coords[0] * i)][currentY + (coords[1] * i)] === currentPlayer)) {
				chainLength++;
				i++;
			}
		});

		return (chainLength >= 4);

	};

	// check whether current player wins. return true if so.
	const isWinner = function (currentX, currentY) {
		return checkDirection(currentX, currentY, 'vertical') ||
			checkDirection(currentX, currentY, 'horizontal') ||
			checkDirection(currentX, currentY, 'diagonal_up') ||
			checkDirection(currentX, currentY, 'diagonal_down');
	};


	const gameBoardVue = new Vue({
		delimiters: delimiters,
		el: "#game-board",
		computed: {
			currentPlayer() {
				return currentPlayer;
			},
			state() {
				return game.state;
			}
		},
		methods: {
			clickColumn: function(col) {
				markNextFree(col)
			}
		},
		created() {
			setupGameBoard();
		}
	});


	const entryVue = new Vue({
		delimiters: delimiters,
		el: "#entry",
		data: {
			gameIdProxy: null,
		},
		methods: {
			updateGameIdProxy: function() {
				this.gameIdProxy = globalGameId
			},
			joinGame: function() {
				console.log('join game')
				setState('play')
				setMultiPlayerMode();
			},
			createGame: function() {
				console.log('create game')
				setState('play')
				setMultiPlayerMode();
			},
			startGame: function() {
				console.log('start game')
				setState('play')
				setSinglePlayerMode();
			}
		},
		computed: {
			gameId: {
				get: function () {
					return this.gameIdProxy;
					},
				set: function (newGameId) {
					game.gameId = newGameId;
					this.updateGameIdProxy();
				}
			},
			state() {
				return game.state;
			}
		},
	})


	const settingsVue = new Vue({
		delimiters: delimiters,
		el: "#setts",
		data: {
			opponentProxy: null
		},
		methods: {
			updateOpponentProxy: function() {
				this.opponentProxy = opponent;
			}
		},
		computed: {
			gameOpponent: {
				get: function () {
					return this.opponentProxy;
					},
				set: function (newOpponent) {
					opponent = newOpponent;
					this.updateOpponentProxy();
				}
			},
			state() {
				return game.state;
			}
		},
		created() {
			this.updateOpponentProxy();
		}
	})
}
