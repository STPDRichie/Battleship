var status_text_start = 'Start game';
var status_text_place_ships = 'Ships placing';
var status_text_battle = 'Battle';

var needs_text_start = 'Click the button to start game';
var needs_text_place = 'Place ship';

var game_status = document.getElementById('game_status');
var game_needs = document.getElementById('game_needs');

game_status.addEventListener('click', function() {
  var response = $.post('/game_button_clicked', {
    current_status: game_status.innerHTML,
    current_needs: game_needs.innerHTML
  });

  response.done(function(data) {
    var content = $(data).find('#content')['prevObject'][0];
    console.log(content);
    game_needs.innerHTML = content['game_needs'];
    game_status.innerHTML = content['game_status'];
    game_status.classList.remove(content['game_status_remove_class']);
    game_status.classList.add(content['game_status_add_class']);
  });

  // if (game_status.innerHTML == status_text_start) {
  //   game_status.innerHTML = status_text_place_ships;
  //   game_needs.innerHTML = needs_text_place;
  //   game_status.classList.remove('game_status');
  //   game_status.classList.add('game_status-inactive');
  // }
  // else if (game_status.innerHTML == status_text_place_ships) {
  //   game_status.innerHTML = status_text_start;
  //   game_needs.innerHTML = needs_text_start;
  //   game_status.classList.remove('game_status-inactive');
  //   game_status.classList.add('game_status');
  // }
  // else if (game_status.innerHTML == status_text_battle) {
  //   game_status.innerHTML = status_text_start;
  // }
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
  var response = $.post('/cell_clicked', {
    board: 'player',
    game_status: game_status.innerHTML,
    cell: cell.id
  });

  response.done(function(data) {
    var content = $(data).find('#content')['prevObject'][0];
    console.log(content);
    if (content['is_changed']) {
      game_status.innerHTML = content['game_status'];
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
  if (game_status.innerHTML != status_text_battle) {
    return;
  }
  else {
    if (cell.innerHTML == solid || cell.innerHTML == circle) {
      cell.innerHTML = crossedCircle;
    }
  }
}