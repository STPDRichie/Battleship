const sleep = ms => new Promise(r => setTimeout(r, ms));

const color_white = '#ffffff';
const color_green = '#95e1d3';
const color_red = '#f38181';
const color_gray = '#d8d8d8';


const game_status = document.getElementById('game_status');
const game_status_battle = 'Battle';
const game_status_win = 'Win';
const game_status_lose = 'Lose';

game_status.addEventListener('click', function () {
  const game_status_click_response = $.post('/status_button_clicked', {
    current_status: game_status.innerHTML
  });

  game_status_click_response.done(function (data) {
    const content = $(data).find('#content')['prevObject'][0];
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
const ship_html_sep = ' - ';
let selected_ship = 'Battleship'

Array.prototype.forEach.call(ship_select_buttons, function (element) {
  element.addEventListener('click', function () {
    changeSelectedShip(element);
  });
});

function changeSelectedShip(ship) {
  let current_ships_count = parseInt(ship.innerHTML.split(ship_html_sep)[1]);
  let current_ship = ship.innerHTML.split(ship_html_sep)[0];
  if (current_ships_count >= 0 && !ship.classList.contains(ship_select_button_class_placed)) {
    let active_ship_button = Array
        .from(ship_select_buttons)
        .find(button => button.classList.contains(ship_select_button_class_active));
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
const board_class_inactive = 'game_board-inactive';
const markup_cell = 'board_markup_cell';
let hovered_cells = [];

Array.prototype.forEach.call(person_cells, function(element) {
  if (!element.classList.contains(markup_cell)) {
    element.addEventListener('click', function () {
      handlePersonBoardClick(element);
    });

    element.addEventListener('mouseover', function () {
      const person_cell_hover_response = $.post('/person_cell_hovered', {
        game_status: game_status.innerHTML,
        current_ship: selected_ship,
        direction: selected_ship_direction,
        cell_id: element.id
      });

      person_cell_hover_response.done(function (data) {
        const content = $(data).find('#content')['prevObject'][0];
        if (content['is_changed']) {
          for (let i = 0; i < content['cells'].length; i++) {
            let current_cell = Array.from(person_cells).find(cell => cell.id === content['cells'][i]);
            hovered_cells.push(current_cell)
            current_cell.style.backgroundColor = color_gray;
          }
        }
      });
    });

    element.addEventListener('mouseout', function () {
      for (let i = 0; i < hovered_cells.length; i++) {
        let current_cell = hovered_cells[i];
        current_cell.style.backgroundColor = color_white;
      }
      hovered_cells = []
    });
  }
});

Array.prototype.forEach.call(opponent_cells, function(element) {
  if (!element.classList.contains(markup_cell)) {
    element.addEventListener('click', async function () {
      if (game_status.innerHTML === game_status_battle) {
        handleOpponentBoardClick(element);
        await sleep(100);
        if (game_status.innerHTML === game_status_win) {
          opponent_board.classList.add(board_class_inactive);
          person_board.classList.add(board_class_inactive);
          game_status.style.color = color_white;
          game_status.style.backgroundColor = color_green;
        }

        opponent_board.classList.add(board_class_inactive);
        await sleep(600);
        if (game_status.innerHTML !== game_status_win && game_status.innerHTML !== game_status_lose) {
          getOpponentTurn();
          await sleep(200);
          opponent_board.classList.remove(board_class_inactive);
        }

        await sleep(100);
        if (game_status.innerHTML === game_status_lose) {
          opponent_board.classList.add(board_class_inactive);
          person_board.classList.add(board_class_inactive);
          game_status.style.color = color_white;
          game_status.style.backgroundColor = color_red;
        }
      }
    });
  }
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
    if (content['is_changed']) {
      game_status.innerHTML = content['game_status'];

      for (let i = 0; i < content['cells'].length; i++) {
        let current_cell = Array.from(person_cells).find(cell => cell.id === content['cells'][i]);
        current_cell.innerHTML = content['cells_icon'];
      }

      if (content['returned_ship'] !== '') {
        let returned_ship = Array
            .from(ship_select_buttons)
            .find(button => button.innerHTML.split(ship_html_sep)[0] === content['returned_ship']);
        if (returned_ship.innerHTML.split(ship_html_sep)[1] === '0') {
          returned_ship.classList.remove(ship_select_button_class_placed);
          returned_ship.classList.add(ship_select_button_class_default);
        }
        returned_ship.innerHTML = content['returned_ship'] + ship_html_sep + content['ship_count'];
        return;
      }

      let current_ship_select_button = Array
          .from(ship_select_buttons)
          .filter(button => button.innerHTML.split(ship_html_sep)[0] === selected_ship)[0];
      current_ship_select_button.innerHTML = selected_ship + ship_html_sep + content['ship_count'];
      if (content['ship_count'] === 0) {
        current_ship_select_button.classList.remove(ship_select_button_class_active);
        current_ship_select_button.classList.add(ship_select_button_class_placed);
        let next_ships = Array
            .from(ship_select_buttons)
            .filter(button => button.innerHTML.split(ship_html_sep)[0] !== selected_ship
                && !button.classList.contains(ship_select_button_class_placed));
        if (next_ships.length !== 0) {
          selected_ship = next_ships[0].innerHTML.split(ship_html_sep)[0];
          let next_ship_select_button = Array
              .from(ship_select_buttons)
              .filter(button => button.innerHTML.split(ship_html_sep)[0] === selected_ship)[0];
          next_ship_select_button.classList.remove(ship_select_button_class_default);
          next_ship_select_button.classList.add(ship_select_button_class_active);
        }
      }

      if (game_status.innerHTML === game_status_battle) {
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
    if (content['is_changed']) {
      game_status.innerHTML = content['game_status'];
      let fired_cell = Array.from(person_cells).find(cell => cell.id === content['cell']);
      fired_cell.innerHTML = content['cell_icon']
    }
  });
}