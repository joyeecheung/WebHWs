// add an event after loading the page
function addLoadEvent(func) {
    var oldonload = window.onload;
    if (typeof window.onload != 'function') {
        window.onload = func;
    } else {
        window.onload = function() {
            oldonload();
            func();
        }
    }
}

// object of pieces
function piece(row, col, id, element) {
    this.row = row;  // in the row of the puzzle
    this.col = col;  // in the column of the puzzle
    this.id = id;  // id-1 is its index in pieces
    this.element = element;  // which element
}

function init() {
    document.getElementById("shufflebutton").onclick = shuffle;
    document.getElementById("select-background").onchange = changeBackground;

    var divs = pieces = document.getElementById("puzzlearea").getElementsByTagName("div");
    pieces = [];
    available = 15;  // the available position is 15

    for(var i = 0; i < 15; i++) {
        var row = Math.floor(i / 4), col = i % 4, id = i + 1;
        divs[i].onclick = onPieceClick;
        pieces[i] = new piece(Math.floor(i / 4), i % 4, i + 1, divs[i]);
        pieces[i].element.style.backgroundPosition = "-" + pieces[i].col*100 + "px -" + pieces[i].row*100 + "px";
    }
    arrange();
}

// arrange pieces and display them
function arrange() {
    for(var i = 0; i < 15; ++i) {
        pieces[i].element.style.left = pieces[i].col*100 + "px";
        pieces[i].element.style.top = pieces[i].row*100 + "px";
    }
}

// shuffle the pieces
function shuffle() {
    var j = 0;
    for(var i = 0; i < 20; ++i) {
        var aRow = Math.floor(available / 4), aCol = available % 4;
        while(Math.abs(pieces[j].row - aRow) + Math.abs(pieces[j].col - aCol) > 1)
            if (j == 14) j = 0;
            else j++;
        // swap position of pieces
        movePiece(j);

        if (j == 14) j = 0;
        else j++;
    }
    arrange();
    update();
}

// change the background of pieces
function changeBackground() {
    var image = document.getElementById("select-background").value;
    for(var i = 0; i < 15; ++i) {
        pieces[i].element.style.backgroundImage = 'url(' + image + ')';
    }
}

function onPieceClick() {
    var cur = parseInt(this.textContent) - 1;
    var aRow = Math.floor(available / 4), aCol = available % 4;

    // not in vicinity
    if(Math.abs(pieces[cur].row - aRow) + Math.abs(pieces[cur].col - aCol) > 1) return;
    
    movePiece(cur);

    update();

    if (isComplete()) {
        alert("You Win!");
        shuffle();
    }
}

function movePiece(cur) {
    var aRow = Math.floor(available / 4), aCol = available % 4;
    available = pieces[cur].row * 4 + pieces[cur].col;
    pieces[cur].col = aCol, pieces[cur].row = aRow;
    pieces[cur].element.style.left = aCol * 100 + "px";
    pieces[cur].element.style.top = aRow * 100 + "px";
}

function update() {
    var aRow = Math.floor(available / 4), aCol = available % 4;

    // change the state of other pieces
    for(var i = 0; i < 15; ++i) {
        if (Math.abs(pieces[i].row - aRow) + Math.abs(pieces[i].col - aCol) > 1)
            pieces[i].element.className = "puzzlepiece";
        else
            pieces[i].element.className += " movablepiece";
    }
}

function isComplete() {
    for(var i = 0; i < 15; i++) {
        if(pieces[i].row * 4 + pieces[i].col != pieces[i].id - 1) {
            return false;
        }
    }
    return true;
}

addLoadEvent(init);