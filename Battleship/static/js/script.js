var status_text_start = 'Start game';
var status_text_place_ships = 'Place your ships';
var status_text_battle = 'Battle';

var game_status_text = document.getElementById('game_status');

game_status_text.addEventListener('click', function() {
  if (game_status_text.innerHTML == status_text_start) {
    game_status_text.innerHTML = status_text_place_ships;
  }
  else if (game_status_text.innerHTML == status_text_place_ships) {
    game_status_text.innerHTML = status_text_start;
  }
  else if (game_status_text.innerHTML == status_text_battle) {
    game_status_text.innerHTML = status_text_start;
  }
});


var solid = '<i class="fa-solid"></i>';
var circle = '<i class="fa-solid fa-circle"></i>';
var crossedCircle = '<i class="fa-solid fa-circle-xmark"></i>';
var emptyCircle = '<i class="fa-regular fa-circle"></i>';

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
  var response = $.post('/', {
    board: 'player',
    game_status: game_status_text.innerHTML,
    cell: cell.id
  });
  response.done(function(data) {
    var content = $(data).find('#content')['prevObject'][0];
    console.log(content);
    if (content['is_changed']) {
      game_status_text.innerHTML = content['game_status'];
      cell.innerHTML = content['cell'];
    }
  })

  // if (game_status_text.innerHTML == status_text_start) {
  //   return;
  // }
  
  // if (game_status_text.innerHTML == status_text_place_ships) {
  //   if (cell.innerHTML == solid) {
  //     cell.innerHTML = circle;
  //   }
  //   else if (cell.innerHTML == circle) {
  //     cell.innerHTML = solid;
  //   }
  // }
  // else if (game_status_text.innerHTML != status_text_battle) {
  //   if (cell.innerHTML == solid) {
  //     cell.innerHTML = circle;
  //   }
  //   else if (cell.innerHTML == circle) {
  //     cell.innerHTML = crossedCircle;
  //   }
  //   else if (cell.innerHTML == crossedCircle) {
  //     cell.innerHTML = solid;
  //   }
  // }
}

function handleAIBoard(cell) {
  if (game_status_text.innerHTML != status_text_battle) {
    return;
  }
  else {
    if (cell.innerHTML == solid || cell.innerHTML == circle) {
      cell.innerHTML = crossedCircle;
    }
  }
}