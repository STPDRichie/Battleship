const sleep = ms => new Promise(r => setTimeout(r, ms));

const game_status = document.getElementById('game_status');

game_status.addEventListener('click', function () {
  const game_status_click_response = $.post('/game_button_clicked', {
    current_status: game_status.innerHTML
  });

  game_status_click_response.done(function (data) {
    const content = $(data).find('#content')['prevObject'][0];
    console.log(content); // TODO HIDE
    if (content['is_changed']) {
      game_status.innerHTML = content['game_status'];
      game_status.classList.remove(content['game_status_remove_class']);
      game_status.classList.add(content['game_status_add_class']);
    }
  });
});


const ship_direction_buttons = document.getElementById('game_ship_direction_select_buttons').getElementsByTagName('*');
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
        .find(button => button !== direction);
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


const ship_select_buttons = document.getElementById('game_ship_select_buttons').getElementsByTagName('*');
const ship_select_button_class_default = 'game_ship_select_button'
const ship_select_button_class_active = 'game_ship_select_button-active';
const ship_select_button_class_placed = 'game_ship_select_button-placed';
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
        .find(button => button.classList.contains('game_ship_select_button-active'));
    active_ship_button.classList.remove(ship_select_button_class_active);
    active_ship_button.classList.add(ship_select_button_class_default);

    selected_ship = current_ship;
    ship.classList.add(ship_select_button_class_active);
    ship.classList.remove(ship_select_button_class_default);
  }
}

const person_board = document.getElementById('person-board');
const person_cells = person_board.getElementsByClassName('board_cell');
const opponent_board = document.getElementById('opponent-board');
const opponent_cells = opponent_board.getElementsByClassName('board_cell');

Array.prototype.forEach.call(person_cells, function(element) {
  element.addEventListener('click', function () {
    handlePersonBoardClick(element);
  });
});

Array.prototype.forEach.call(opponent_cells, function(element) {
  element.addEventListener('click', async function () {
    handleOpponentBoardClick(element);
    await sleep(100);
    if (game_status.innerHTML === 'Win') {
      opponent_board.classList.add('game_board-inactive');
      person_board.classList.add('game_board-inactive');
      game_status.style.color = '#ffffff'
      game_status.style.backgroundColor = '#95e1d3';
    }

    opponent_board.classList.add('game_board-inactive');
    await sleep(600);
    if (game_status.innerHTML !== 'Win' && game_status.innerHTML !== 'Lose') {
      getOpponentTurn();
      await sleep(200);
      opponent_board.classList.remove('game_board-inactive');
    }

    await sleep(100);
    if (game_status.innerHTML === 'Lose') {
      opponent_board.classList.add('game_board-inactive');
      person_board.classList.add('game_board-inactive');
      game_status.style.color = '#ffffff'
      game_status.style.backgroundColor = '#f38181';
    }
  });
});

function handlePersonBoardClick(cell) {
  const person_board_click_response = $.post('/person_cell_clicked', {
    direction: selected_ship_direction,
    game_status: game_status.innerHTML,
    current_ship: selected_ship,
    cell_icon: cell.innerHTML,
    cell_id: cell.id
  });

  person_board_click_response.done(function (data) {
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
            .find(button => button.innerHTML.split(' - ')[0] === content['returned_ship']);
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
        document.getElementById('game_ship_direction_select_buttons').style.display = 'none';
        document.getElementById('game_ship_select_buttons').style.display = 'none';
      }
    }
  });
}

function handleOpponentBoardClick(cell) {
  const opponent_board_click_response = $.post('/opponent_cell_clicked', {
    game_status: game_status.innerHTML,
    cell_id: cell.id
  });

  opponent_board_click_response.done(function (data) {
    const content = $(data).find('#content')['prevObject'][0];
    console.log(content); // TODO HIDE
    if (content['is_changed']) {
      game_status.innerHTML = content['game_status'];
      cell.innerHTML = content['cell_icon'];
    }
  });
}

function getOpponentTurn() {
  const opponent_fire = $.post('/get_opponent_fire', {
    game_status: game_status.innerHTML
  });

  opponent_fire.done(function (data) {
    const content = $(data).find('#content')['prevObject'][0];
    console.log(content); // TODO HIDE
    if (content['is_changed']) {
      game_status.innerHTML = content['game_status'];
      let fired_cell = Array.from(person_cells).find(cell => cell.id === content['cell']);
      fired_cell.innerHTML = content['cell_icon']
    }
  });
}