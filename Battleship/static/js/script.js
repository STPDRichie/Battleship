const game_status = document.getElementById('game_status');
const game_needs = document.getElementById('game_needs');

game_status.addEventListener('click', function() {
  const response = $.post('/game_button_clicked', {
    current_status: game_status.innerHTML,
    current_needs: game_needs.innerHTML
  });

  response.done(function(data) {
    const content = $(data).find('#content')['prevObject'][0];
    console.log(content); // TODO HIDE
    game_needs.innerHTML = content['game_needs'];
    game_status.innerHTML = content['game_status'];
    game_status.classList.remove(content['game_status_remove_class']);
    game_status.classList.add(content['game_status_add_class']);
  });
});


const game_ship_directions = document.getElementById('game_ship_direction_choise_buttons').getElementsByTagName('*');
const game_ship_direction_active = 'game_ship_direction-active'
const game_ship_direction_inactive = 'game_ship_direction'
let ship_direction = 'Vertical';

Array.prototype.forEach.call(game_ship_directions, function (element) {
  element.addEventListener('click', function() {
    if (element.classList.contains(game_ship_direction_inactive)) {
      element.classList.add(game_ship_direction_active);
      element.classList.remove(game_ship_direction_inactive);

      let other_button = Array.from(game_ship_directions).filter(button => button !== element)[0];
      other_button.classList.add(game_ship_direction_inactive);
      other_button.classList.remove(game_ship_direction_active);

      if (ship_direction === 'Vertical') {
        ship_direction = 'Horizontal';
      }
      else if (ship_direction === 'Horizontal') {
        ship_direction = 'Vertical';
      }
    }
  })
})


const player_cells = document.getElementById('player-board').getElementsByClassName('board_cell');
const ai_cells = document.getElementById('ai-board').getElementsByClassName('board_cell');

Array.prototype.forEach.call(player_cells, function(element) {
	element.addEventListener('click', function() {
    handlePlayerBoardClick(element);
	});
});

Array.prototype.forEach.call(ai_cells, function(element) {
  element.addEventListener('click', function() {
    handleAIBoardClick(element);
  });
});

function handlePlayerBoardClick(cell) {
  const response = $.post('/player_cell_clicked', {
    direction: ship_direction,
    game_status: game_status.innerHTML,
    current_needs: game_needs.innerHTML,
    cell_icon: cell.innerHTML,
    cell_id: cell.id
  });

  response.done(function(data) {
    const content = $(data).find('#content')['prevObject'][0];
    console.log(content); // TODO HIDE
    if (content['is_changed']) {
      game_status.innerHTML = content['game_status'];

      let current_board = Array.from(player_cells);
      for (let i = 0; i < content['cells'].length; i++) {
        let current_cell = current_board.find(cell => cell.id === content['cells'][i]);
        current_cell.innerHTML = content['cells_icon'];
      }
    }
  });
}

function handleAIBoardClick(cell) {
  const response = $.post('/ai_cell_clicked', {
    game_status: game_status.innerHTML,
    cell_icon: cell.innerHTML,
    cell_id: cell.id
  });

  response.done(function(data) {
    const content = $(data).find('#content')['prevObject'][0];
    console.log(content); // TODO HIDE
    if (content['is_changed']) {
      game_status.innerHTML = content['game_status'];
      cell.innerHTML = content['cell_icon']
    }
  });
}