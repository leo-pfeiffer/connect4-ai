(function() {

	const ConnectFour = function () {

		const getOpponent = function() {
			const ele = document.getElementsByName('opponent');

			for(let i = 0; i < ele.length; i++) {
				if(ele[i].checked){
					opponent = ele[i].value;
					alert(ele[i].value + ' selected.');
				}
			}
        };

		const getMoveFromAI = function () {

			if (opponent === 'Human'){
				return;
			}

			let dataToSend = [gameBoard, opponent];
			dataToSend = JSON.stringify({ 'list': dataToSend });

			// POST
			fetch('/ai-action', {

				method: 'POST',

				// JSON payload: pass gameBoard to Flask
				body: dataToSend
			}).then(function (response) {
				return response.text();

			}).then(function (col) {
				console.log('AI played column ' + col);
				return col;

			}).then(markNextFree);

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
					(gameBoard[currentX + (coords[0] * i)][currentY + (coords[1] * i)] === currentPlayer)
					) {
					chainLength = chainLength + 1;
					console.log(direction, currentX, currentY, currentX + (coords[0] * i), currentY + (coords[1] * i));
					i = i + 1;
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

		// clearBoard after end of game
		const clearBoard = function () {

			// reset attributes
			Array.prototype.forEach.call(document.querySelectorAll('circle'), function (piece) {
				piece.setAttribute('class', 'free');
			});

			// reset gameBoard
			gameBoard = {};

			for (let x = 0; x <= numRows; x++) {

				gameBoard[x] = {};

				for (let y = 0; y <= numCols; y++) {
					gameBoard[x][y] = 'free';
				}
			}

			// reset turns
			numTurns = 0;

			// reset opponent selection
			opponent = "None";

			// reset Player
			currentPlayer = 'red';

			return gameBoard;

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

			if (nextY === false) {
				alert('Column full. Choose another.');
				return false;
			}

			// mark free position with piece of current player
			gameBoard[x][nextY] = currentPlayer;

			// set the attribute of the played position to currentPlayer ('red' or 'yellow')
			document.querySelector('#column-' + x + ' .row-' + nextY + ' circle').setAttribute(
				'class', currentPlayer
			);

			// check if game is over
			if (isWinner(parseInt(x), nextY)) {
				alert(currentPlayer + ' wins!');
				clearBoard();
				return true;
			}

			numTurns = numTurns + 1;

			if (numTurns >= numRows * numCols) {
				alert('DRAW!');
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

		// check whether a coordinate is on the board
		const onBoard = function (x, y) {
			return (gameBoard.hasOwnProperty(x) && typeof gameBoard[x][y] !== 'undefined');

		};

		let gameBoard = {};
		let currentPlayer = 'red';
		let numRows = 6;
		let numCols = 7;
		let numTurns = 0;
		let opponent = "None";

		let _init = function () {

			alert("You are playing as 'red'.\nSelect you opponent below.")

			// initiate gameBoard with all positions free
			for (let x = 0; x <= numRows; x++) {

				gameBoard[x] = {};

				for (let y = 0; y <= numCols; y++) {
					gameBoard[x][y] = 'free';
				}
			}

			let columns;
			// get all columns from html file
			columns = document.querySelectorAll('.column');

			// add EventListener to all columns. Whenever new click => Add new piece
			// here: for one player, substitute EventListener with AI Selector
			Array.prototype.forEach.call(columns, function (col) {
				col.addEventListener('click', function () {
					markNextFree(col.getAttribute('data-x'));
				});
			});

			let opponentSelect;

			opponentSelect = document.querySelector('button');
			opponentSelect.addEventListener('click', getOpponent);

		};

		_init();

	};

	ConnectFour();

})();