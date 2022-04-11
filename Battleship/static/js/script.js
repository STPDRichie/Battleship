const game_status = document.getElementById('game_status');

game_status.addEventListener('click', function () {
  const response = $.post('/game_button_clicked', {
    current_status: game_status.innerHTML
  });

  response.done(function(data) {
    const content = $(data).find('#content')['prevObject'][0];
    console.log(content); // TODO HIDE
    if (content['is_changed']) {
      game_status.innerHTML = content['game_status'];
      game_status.classList.remove(content['game_status_remove_class']);
      game_status.classList.add(content['game_status_add_class']);
    }
  });
});


const ship_direction_buttons = document.getElementById('game_ship_direction_choise_buttons').getElementsByTagName('*');
const ship_direction_class_selected = 'game_ship_direction-active'
const ship_direction_class_not_selected = 'game_ship_direction'
let selected_ship_direction = 'Vertical';

Array.prototype.forEach.call(ship_direction_buttons, function (element) {
  element.addEventListener('click', function () {
    changeShipDirection(element);
  });
});

function changeShipDirection(direction) {
  if (direction.classList.contains(ship_direction_class_not_selected)) {
    direction.classList.add(ship_direction_class_selected);
    direction.classList.remove(ship_direction_class_not_selected);

    let other_button = Array
        .from(ship_direction_buttons)
        .filter(button => button !== direction)[0];
    other_button.classList.add(ship_direction_class_not_selected);
    other_button.classList.remove(ship_direction_class_selected);

    if (selected_ship_direction === 'Vertical') {
      selected_ship_direction = 'Horizontal';
    }
    else if (selected_ship_direction === 'Horizontal') {
      selected_ship_direction = 'Vertical';
    }
  }
}


const ship_select_buttons = document.getElementById('game_ship_choise_buttons').getElementsByTagName('*');
const ship_select_button_class_default = 'game_ship_choise_button'
const ship_select_button_class_active = 'game_ship_choise_button-active';
const ship_select_button_class_placed = 'game_ship_choise_button-placed';
let selected_ship = 'Battleship'

Array.prototype.forEach.call(ship_select_buttons, function (element) {
  element.addEventListener('click', function () {
    changeSelectedShip(element);
  });
});

function changeSelectedShip(ship) {
  let current_ships_count = parseInt(ship.innerHTML.split(' - ')[1]);
  let current_ship = ship.innerHTML.split(' - ')[0];
  if (current_ships_count >= 0 && !ship.classList.contains(ship_select_button_class_placed)) {
    let active_ship_button = Array
        .from(ship_select_buttons)
        .filter(button => button.classList.contains('game_ship_choise_button-active'))[0];
    active_ship_button.classList.remove(ship_select_button_class_active);
    active_ship_button.classList.add(ship_select_button_class_default);

    selected_ship = current_ship;
    ship.classList.add(ship_select_button_class_active);
    ship.classList.remove(ship_select_button_class_default);
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
    direction: selected_ship_direction,
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

      if (content['returned_ship'] !== '') {
        let returned_ship = Array
            .from(ship_select_buttons)
            .filter(button => button.innerHTML.split(' - ')[0] === content['returned_ship'])[0];
        if (returned_ship.innerHTML.split(' - ')[1] === '0') {
          returned_ship.classList.remove(ship_select_button_class_placed);
          returned_ship.classList.add(ship_select_button_class_default);
        }
        returned_ship.innerHTML = content['returned_ship'] + ' - ' + content['ship_count'];
        return;
      }

      let current_ship_choise_button = Array
          .from(ship_select_buttons)
          .filter(button => button.innerHTML.split(' - ')[0] === selected_ship)[0];
      current_ship_choise_button.innerHTML = selected_ship + ' - ' + content['ship_count'];
      if (content['ship_count'] === 0) {
        current_ship_choise_button.classList.remove(ship_select_button_class_active);
        current_ship_choise_button.classList.add(ship_select_button_class_placed);
        let next_ships = Array
            .from(ship_select_buttons)
            .filter(button => button.innerHTML.split(' - ')[0] !== selected_ship
                && !button.classList.contains(ship_select_button_class_placed));
        if (next_ships.length !== 0) {
          selected_ship = next_ships[0].innerHTML.split(' - ')[0];
          let next_ship_choise_button = Array
              .from(ship_select_buttons)
              .filter(button => button.innerHTML.split(' - ')[0] === selected_ship)[0];
          next_ship_choise_button.classList.remove(ship_select_button_class_default);
          next_ship_choise_button.classList.add(ship_select_button_class_active);
        }
      }

      if (game_status.innerHTML === 'Battle') {
        let active_button = Array
            .from(ship_direction_buttons)
            .filter(button => button.classList.contains(ship_direction_class_not_selected))[0];
        active_button.classList.remove(ship_direction_class_not_selected);
        active_button.classList.add(ship_direction_class_selected);
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