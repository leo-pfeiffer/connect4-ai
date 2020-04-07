(function() {

	const ConnectFour = function () {

		const checkDirection = function (currentX, currentY, direction) {

			let chainLength, directions;

			directions = {
				horizontal: [
					[0, -1], [0, 1]
				],
				vertical: [
					[-1, 0], [1, 0]
				],
				diagonal: [
					[-1, -1], [1, 1], [-1, 1], [1, -1]
				]
			};

			chainLength = 1;

			directions[direction].forEach(function (coords) {

				let i = 1;

				while (isBounds(currentX + (coords[0] * i), currentY + (coords[1] * i)) &&
					(gameBoard[currentX + (coords[0] * i)][currentY + (coords[1] * i)] === currentPlayer)
					) {
					chainLength = chainLength + 1;
					i = i + 1;
				}

			});

			return (chainLength >= 4);

		};
		const isWinner = function (currentX, currentY) {
			return checkDirection(currentX, currentY, 'vertical') ||
				checkDirection(currentX, currentY, 'diagonal') ||
				checkDirection(currentX, currentY, 'horizontal');
		};
		const clearBoard = function () {

			Array.prototype.forEach.call(document.querySelectorAll('circle'), function (piece) {
				piece.setAttribute('class', 'free');
			});

			gameBoard = {};

			for (let x = 0; x <= numRows; x++) {

				gameBoard[x] = {};

				for (let y = 0; y <= numCols; y++) {
					gameBoard[x][y] = 'free';
				}

				console.log(gameBoard);
			}

			numTurns = 0;

			return gameBoard;

		};
		const markNextFree = function (x) {

			let nextY;

			nextY = false;

			for (let y = 0; y < numRows; y++) {
				if (gameBoard[x][y] === 'free') {
					nextY = y;
					break;
				}
			}

			if (nextY === false) {
				alert('No free spaces in this column. Try another.');
				return false;
			}

			gameBoard[x][nextY] = currentPlayer;

			document.querySelector('#column-' + x + ' .row-' + nextY + ' circle').setAttribute(
				'class', currentPlayer
			);

			if (isWinner(parseInt(x), nextY)) {
				alert(currentPlayer + ' wins!');
				clearBoard();
				return true;
			}

			numTurns = numTurns + 1;

			if (numTurns >= numRows * numCols) {
				alert('It\'s a tie!');
				clearBoard();
				return true;
			}

			currentPlayer = currentPlayer === 'red' ? 'yellow' : 'red';

		};

		let gameBoard = {};
		let currentPlayer = 'red';
		let numRows = 6;
		let numCols = 7;
		let numTurns = 0;

		let _init = function () {

			let columns;

			columns = document.querySelectorAll('.column');

			Array.prototype.forEach.call(columns, function (col) {
				col.addEventListener('click', function () {
					markNextFree(col.getAttribute('data-x'));
				});
			});

			for (let x = 0; x <= numRows; x++) {

				gameBoard[x] = {};

				for (let y = 0; y <= numCols; y++) {
					gameBoard[x][y] = 'free';
				}
			}
		};


		const isBounds = function (x, y) {
			return (gameBoard.hasOwnProperty(x) && typeof gameBoard[x][y] !== 'undefined');
		};


		_init();

	};

	ConnectFour();

})();

