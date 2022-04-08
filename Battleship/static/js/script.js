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
  const response = $.post('/cell_clicked', {
    board: 'player',
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
      cell.innerHTML = content['cell'];
    }
  });
}

function handleAIBoardClick(cell) {
  const response = $.post('/cell_clicked', {
    board: 'ai',
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
      cell.innerHTML = content['cell'];
    }
  });
}