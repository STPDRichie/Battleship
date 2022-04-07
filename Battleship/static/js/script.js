var game_status_text = document.getElementById('game_status');
game_status_text.addEventListener('click', function() {
  if (game_status_text.innerHTML == 'Start game') {
    game_status_text.innerHTML = 'Place your ships';
  }
  else if (game_status_text.innerHTML == 'Place your ships') {
    game_status_text.innerHTML = 'Start game';
  }
});

var solid = '<i class="fa-solid"></i>';
var circle = '<i class="fa-solid fa-circle"></i>';
var crossedCircle = '<i class="fa-solid fa-circle-xmark"></i>';

var player_cells = document.getElementById('player-board').getElementsByClassName('board_cell');
var ai_cells = document.getElementById('ai-board').getElementsByClassName('board_cell');

Array.prototype.forEach.call(player_cells, function(element) {
	element.addEventListener('click', function() {
    handlePlayerBoard(element);
	});
});

Array.prototype.forEach.call(ai_cells, function(element) {
  element.addEventListener('click', function() {
    handleAIBoard(element);
  });
});

function handlePlayerBoard(cell) {
  if (game_status_text.innerHTML != 'Start game') {
    if (cell.innerHTML == solid) {
      cell.innerHTML = circle;
    }
    else if (cell.innerHTML == circle) {
      cell.innerHTML = crossedCircle;
    }
    else if (cell.innerHTML == crossedCircle) {
      cell.innerHTML = solid;
    }
  }
}

function handleAIBoard(cell) {
  if (game_status_text.innerHTML == 'Place your ships') {
    return;
  }
  if (game_status_text.innerHTML != 'Start game') {
    if (cell.innerHTML == solid || cell.innerHTML == circle) {
      cell.innerHTML = crossedCircle;
    }
  }
}