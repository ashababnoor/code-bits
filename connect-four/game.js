let player1 = 'Player A';
// player1 = prompt('Player One: Enter your name. (You will be blue)', player1);

if (player1 === "") {
    // user pressed OK, but the input field was empty
    player1 = 'Player A'
} else if (player1) {
    // user typed something and hit OK
} else {
    // user hit cancel
    player1 = 'Player A'
}

let player1_color = '#0071BC'


let player2 = 'Player B';
// player2 = prompt('Player Two: Enter your name. (You will be red)', player2);

if (player2 === "") {
    // user pressed OK, but the input field was empty
    player2 = 'Player B'
} else if (player2) {
    // user typed something and hit OK
} else {
    // user hit cancel
    player2 = 'Player B'
}

let player2_color = '#D4145A'


let grey = 'rgb(128, 128, 128)';

let game_active = true;
let table = $('table tr');

let buttons = $('button');

function reportWin(rowNum, colNum) {
    console.log("You won starting at this row, col");
    console.log('Row', rowNum, 'Column', colNum);
}

function changeColor(rowIndex, colIndex, color) {
    return table.eq(rowIndex).find('td').eq(colIndex).find('button').css('background-color', color);
}

function getColor(rowIndex, colIndex) {
    return table.eq(rowIndex).find('td').eq(colIndex).find('button').css('background-color');
}

function checkBottom(colIndex) {
    let colorReport;
    for (var row = 5; row >= 0; row--) {
        colorReport = getColor(row, colIndex);
        if (colorReport == grey) {
            return row;
        }
    }
}

function colorMatchCheck(one, two, three, four) {
    return (
        one === two &&
        one === three &&
        one === four &&
        one !== grey &&
        one !== undefined
    )
}

function horizontalWinCheck() {
    for (var row = 0; row < 6; row++) {
        for (var col = 0; col < 4; col++) {
            if (colorMatchCheck(
                    getColor(row, col + 0),
                    getColor(row, col + 1),
                    getColor(row, col + 2),
                    getColor(row, col + 3)
                )) {
                console.log('Horizontal win');
                reportWin(row, col);
                return true;
            } else {
                continue;
            }
        }
    }
}

function verticalWinCheck() {
    for (var col = 0; col < 7; col++) {
        for (var row = 0; row < 3; row++) {
            if (colorMatchCheck(
                    getColor(row + 0, col),
                    getColor(row + 1, col),
                    getColor(row + 2, col),
                    getColor(row + 3, col)
                )) {
                console.log('Vertical win');
                reportWin(row, col);
                return true;
            } else {
                continue;
            }
        }
    }
}

function diagonalWinCheck() {
    for (var col = 0; col < 5; col++) {
        for (var row = 0; row < 7; row++) {
            if (colorMatchCheck(
                    getColor(row + 0, col + 0),
                    getColor(row + 1, col + 1),
                    getColor(row + 2, col + 2),
                    getColor(row + 3, col + 3)
                )) {
                console.log('Diagonal win');
                reportWin(row, col);
                return true;
            } else if (colorMatchCheck(
                    getColor(row - 0, col + 0),
                    getColor(row - 1, col + 1),
                    getColor(row - 2, col + 2),
                    getColor(row - 3, col + 3)
                )) {
                console.log('diagonal win');
                reportWin(row, col);
                return true;
            } else {
                continue;
            }
        }
    }
}


let currPlayer = 1;
let currName = player1;
let currColor = player1_color;

$('h3').text(currName + " it is your turn, pick a column to drop in!");

$('.board button').on('click', function() {
    if (game_active) {
        let col = $(this).closest('td').index();
        let bottomAvail = checkBottom(col);

        changeColor(bottomAvail, col, currColor);
        if (bottomAvail == 0) {
            $('button#chip-0' + (col + 1)).prop('disabled', true);
        }

        if (horizontalWinCheck() || verticalWinCheck() || diagonalWinCheck()) {
            $('h1').text(currName + " you have won!");
            $('h2').fadeOut('fast');
            $('h3').text('(Reload page to play again!)');
            game_active = false;
        } else {
            currPlayer = currPlayer * -1;

            if (currPlayer == 1) {
                currName = player1;
                currColor = player1_color;
                $('h3').text(currName + " it is your turn, pick a column to drop in!");
            } else {
                currName = player2;
                currColor = player2_color;
                $('h3').text(currName + " it is your turn, pick a column to drop in!");
            }
        }
    }
})