const game_status = document.getElementById('game_status');

game_status.addEventListener('click', function () {
  const response = $.post('/game_button_clicked', {
    current_status: game_status.innerHTML
  });

  response.done(function(data) {
    const content = $(data).find('#content')['prevObject'][0];
    console.log(content); // TODO HIDE
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
  element.addEventListener('click', function () {
    changeShipDirection(element);
  });
});

function changeShipDirection(direction) {
  if (direction.classList.contains(game_ship_direction_inactive)) {
    direction.classList.add(game_ship_direction_active);
    direction.classList.remove(game_ship_direction_inactive);

    let other_button = Array
        .from(game_ship_directions)
        .filter(button => button !== direction)[0];
    other_button.classList.add(game_ship_direction_inactive);
    other_button.classList.remove(game_ship_direction_active);

    if (ship_direction === 'Vertical') {
      ship_direction = 'Horizontal';
    }
    else if (ship_direction === 'Horizontal') {
      ship_direction = 'Vertical';
    }
  }
}


const game_ship_choise_buttons = document.getElementById('game_ship_choise_buttons').getElementsByTagName('*');
const ship_select_button_default = 'game_ship_choise_button'
const ship_select_button_active = 'game_ship_choise_button-active';
const ship_select_button_placed = 'game_ship_choise_button-placed';
let selected_ship = 'Battleship'

Array.prototype.forEach.call(game_ship_choise_buttons, function (element) {
  element.addEventListener('click', function () {
    changeSelectedShip(element);
  });
});

function changeSelectedShip(ship) {
  let current_ships_count = parseInt(ship.innerHTML.split(' - ')[1]);
  let current_ship = ship.innerHTML.split(' - ')[0];
  if (current_ships_count >= 0 && !ship.classList.contains(ship_select_button_placed)) {
    let active_ship_button = Array
        .from(game_ship_choise_buttons)
        .filter(button => button.classList.contains('game_ship_choise_button-active'))[0];
    active_ship_button.classList.remove(ship_select_button_active);
    active_ship_button.classList.add(ship_select_button_default);

    selected_ship = current_ship;
    ship.classList.add(ship_select_button_active);
    ship.classList.remove(ship_select_button_default);
  }
}


const person_cells = document.getElementById('person-board').getElementsByClassName('board_cell');
const opponent_cells = document.getElementById('opponent-board').getElementsByClassName('board_cell');

Array.prototype.forEach.call(person_cells, function(element) {
  element.addEventListener('click', function () {
    handlePersonBoardClick(element);
  });
});

Array.prototype.forEach.call(opponent_cells, function(element) {
  element.addEventListener('click', function () {
    handleOpponentBoardClick(element);
  });
});

function handlePersonBoardClick(cell) {
  const response = $.post('/person_cell_clicked', {
    direction: ship_direction,
    game_status: game_status.innerHTML,
    current_ship: selected_ship,
    cell_icon: cell.innerHTML,
    cell_id: cell.id
  });

  response.done(function(data) {
    const content = $(data).find('#content')['prevObject'][0];
    console.log(content); // TODO HIDE
    if (content['is_changed']) {
      game_status.innerHTML = content['game_status'];

      let current_board = Array.from(person_cells);
      for (let i = 0; i < content['cells'].length; i++) {
        let current_cell = current_board.find(cell => cell.id === content['cells'][i]);
        current_cell.innerHTML = content['cells_icon'];
      }
    }
  });
}

function handleOpponentBoardClick(cell) {
  const response = $.post('/opponent_cell_clicked', {
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