const sleep = ms => new Promise(r => setTimeout(r, ms));

const color_white = '#ffffff';
const color_lightgray = '#999999';
const color_darkgray = '#333333';
const color_green = '#95e1d3';
const color_red = '#f38181';
const color_cell_hovered_gray = '#d8d8d8';
const color_section_gray = '#eeeeee';

const icon_destroyed = '<i class="fa-solid fa-circle-xmark"></i>'
const icon_empty = '<i class="fa-solid"></i>'


const game_session_section = document.getElementById('game-session');
const game_select_block = document.getElementById('game-select-block');
const lobby_block = document.getElementById('lobby-block');
const host_block = document.getElementById('host-lobby-block');
const member_block = document.getElementById('member-lobby-block');
const member_lobby_status = document.getElementById('member-lobby-status');
const member_lobby_status_text_waiting = 'Waiting for host';
const member_lobby_status_text_left = 'Host left';

const play_with_robot_button = document.getElementById('play-with-robot-button');
const username = document.getElementById('username');
const host_button = document.getElementById('host-button');
const session_key = document.getElementById('user-session-key');
const start_button = document.getElementById('start-button');
const session_key_input = document.getElementById('session-key-input');
const connect_button = document.getElementById('connect-button');
const leave_button = document.getElementById('leave-button');
const hosts_opponent = document.getElementById('host-opponent');
const members_opponent = document.getElementById('join-opponent');

const game_session_button_class_default = 'game-session__button';
const game_session_button_class_inactive = 'game-session__button_inactive';
const session_key_cookie_name_eq = 'session-key=';
const session_key_cookie_erase_id = session_key_cookie_name_eq + '; Max-Age=0';
let is_opponent_ai = false;
let is_game_started = false;

username.value = 'Guest';
session_key.innerHTML = Date.now().toString();


window.onbeforeunload = leave

function leave() {
  const disconnect_response = $.post('/leave', {
    username: username.value
  });
  
  disconnect_response.done(function (data) {
    if (data['is_changed']) {
      document.cookie = session_key_cookie_erase_id;
    }
  });
}


leave_button.addEventListener('click', function () {
  leave();
  
  host_block.style.display = 'none';
  member_block.style.display = 'none';
  lobby_block.style.display = 'none';
  
  game_select_block.style.display = 'block';
});


play_with_robot_button.addEventListener('click', function () {
  $.post('host_lobby', {
    session_key: session_key.innerHTML,
    username: username.value
  });
  
  is_opponent_ai = true;
  game_session_section.style.display = 'none';
  game_panel_section.style.display = 'block';
  game_section.style.display = 'flex';
});


host_button.addEventListener('click', function () {
  if (username.value === '') {
    return;
  }
  
  const host_response = $.post('/host_lobby', {
    session_key: session_key.innerHTML,
    username: username.value
  });
  
  host_response.done(function (data) {
    if (data['is_lobby_exist']) {
      game_select_block.style.display = 'none';
      lobby_block.style.display = 'block';
      host_block.style.display = 'flex';
  
      waitForMemberConnect();
    }
  });
});

function waitForMemberConnect() {
  if (is_game_started) {
    return;
  }
  
  $.ajax({
    url: '/wait_for_member_connect',
    timeout: 30000,
    success: function(data) {
      if (!data['is_lobby_exist']) {
        return;
      }
      
      if (data['is_changed']) {
        hosts_opponent.innerHTML = data['opponent'];
        start_button.classList.add(game_session_button_class_default);
        start_button.classList.remove(game_session_button_class_inactive);
        checkForMemberConnection();
      } else {
        waitForMemberConnect();
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.log('wait_for_member_connect: ' + jqXHR.status + ", " + textStatus + ", " + errorThrown);
      waitForMemberConnect();
    }
  });
}

function checkForMemberConnection() {
  if (is_game_started) {
    return;
  }
  
  $.ajax({
    url: '/check_for_member_connection',
    timeout: 30000,
    success: function (data) {
      if (data['opponent'] === '') {
        hosts_opponent.innerHTML = '';
        start_button.classList.add(game_session_button_class_inactive);
        start_button.classList.remove(game_session_button_class_default);
        waitForMemberConnect();
      } else {
        checkForMemberConnection();
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.log('check_for_member_connection: ' + jqXHR.status + ", " + textStatus + ", " + errorThrown);
      checkForMemberConnection();
    }
  });
}


start_button.addEventListener('click', function () {
  if (hosts_opponent.innerHTML === '') {
    return;
  }
  
  game_session_section.style.display = 'none';
  game_panel_section.style.display = 'block';
  game_section.style.display = 'flex';
  
  const start_click_response = $.post('/start_game', {
    current_status: game_status.innerHTML
  });
  
  start_click_response.done(function (data) {
    if (data['is_changed']) {
      is_game_started = true;
      showGameUI(data['game_status'].toString());
    }
  });
});


connect_button.addEventListener('click', function () {
  if (username.value === '' || session_key_input.value === '') {
    return;
  }
  
  const connect_button_click_response = $.post('/connect_to_lobby', {
    session_key: session_key_input.value,
    username: username.value
  });
  
  connect_button_click_response.done(function (data) {
    if (!data['is_lobby_exist']) {
      // todo alert lobby is not exist
    }
    
    if (data['is_changed']) {
      members_opponent.innerHTML = data['opponent'];
      
      game_select_block.style.display = 'none';
      lobby_block.style.display = 'block';
      member_block.style.display = 'flex';
      member_lobby_status.innerHTML = member_lobby_status_text_waiting;
  
      waitForStartGame();
    } else {
      // todo alert same name
    }
  });
});

function waitForStartGame() {
  $.ajax({
    url: '/check_for_start_game',
    timeout: 30000,
    success: function (data) {
      if (data['is_changed']) {
        if (!data['is_lobby_exist']) {
          members_opponent.innerHTML = '';
          member_lobby_status.innerHTML = member_lobby_status_text_left;
          leave();
        } else {
          is_game_started = true;
          game_session_section.style.display = 'none';
          game_panel_section.style.display = 'block';
          game_section.style.display = 'flex';
          showGameUI(game_status_placing_ships);
        }
      } else {
        waitForStartGame();
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.log('check_for_start_game: ' + jqXHR.status + ", " + textStatus + ", " + errorThrown);
      waitForStartGame();
    }
  });
}


const game_panel_section = document.getElementById('game-panel');
const game_status = document.getElementById('game-status');
const ship_placing_buttons = document.getElementById('ship-placing-buttons');
const game_status_active_class = 'game-panel__status';
const game_status_inactive_class = 'game-panel__status_inactive'
const game_status_placing_ships = 'Ships placing';
const game_status_battle = 'Battle';
const game_status_win = 'Win';
const game_status_lose = 'Lose';

const restart_button = document.getElementById('game-restart-button');


const ship_direction_buttons = document.getElementById('ship-direction-select-buttons').getElementsByTagName('*');
const ship_direction_default_button = document.getElementById('ship-direction-vertical');
const ship_direction_class_selected = 'game-panel__ship-direction_active'
const ship_direction_class_not_selected = 'game-panel__ship-direction'
const direction_vertical = 'Vertical';
const direction_horizontal = 'Horizontal';
let selected_ship_direction = 'Vertical';


const ship_select_buttons = document.getElementById('ship-select-buttons').getElementsByTagName('*');
const ship_select_default_button = document.getElementById('battleship-select-button');
const battleship_select_button = document.getElementById('battleship-select-button');
const cruiser_select_button = document.getElementById('cruiser-select-button');
const submarine_select_button = document.getElementById('submarine-select-button');
const destroyer_select_button = document.getElementById('destroyer-select-button');

const ship_select_button_class_default = 'game-panel__ship-select-button'
const ship_select_button_class_active = 'game-panel__ship-select-button_active';
const ship_select_button_class_inactive = 'game-panel__ship-select-button_inactive';

const battleship_select_button_default_inner = 'Battleship - 1';
const cruiser_select_button_default_inner = 'Cruiser - 2';
const submarine_select_button_default_inner = 'Submarine - 3';
const destroyer_select_button_default_inner = 'Destroyer - 4';
const ship_count_sep = ' - ';
const ship_select_button_default = 'Battleship'
let selected_ship = 'Battleship'


const remaining_ships = document.getElementsByClassName('remaining-ship__count');
const remaining_ship_panel = document.getElementById('remaining-ships-panel');
const remaining_ship_count_id_template = '-remaining-ship-count__';


const game_section = document.getElementById('game');
const person_board = document.getElementById('person-board');
const person_cells = person_board.getElementsByClassName('game__cell');
const opponent_board = document.getElementById('opponent-board');
const opponent_cells = opponent_board.getElementsByClassName('game__cell');
const board_class_inactive = 'game__board_inactive';
const markup_cell_class = 'game__markup-cell';
let hovered_cells = [];


game_status.addEventListener('click', function () {
  const game_status_click_response = $.post('/start_game', {
    current_status: game_status.innerHTML
  });
  
  game_status_click_response.done(function (data) {
    showGameUI(data['game_status'].toString());
  });
});

function showGameUI(new_game_status) {
  game_status.innerHTML = new_game_status;
  game_status.classList.remove(game_status_active_class);
  game_status.classList.add(game_status_inactive_class);

  ship_placing_buttons.style.display = 'block';
  restart_button.style.display = 'flex';
}


restart_button.addEventListener('click', function () {
  const restart_button_click_response = $.get('/restart_game');
  
  restart_button_click_response.done(function (data) {
    if (data['is_changed']) {
      resetGame();
    }
  });
});

function resetGame() {
  game_status.innerHTML = game_status_placing_ships;
  game_status.style.color = color_lightgray;
  game_status.style.backgroundColor = color_section_gray;
  ship_placing_buttons.style.display = 'block';
  remaining_ship_panel.style.display = 'none';
  
  changeShipDirection(ship_direction_default_button);
  battleship_select_button.innerHTML = battleship_select_button_default_inner;
  cruiser_select_button.innerHTML = cruiser_select_button_default_inner;
  submarine_select_button.innerHTML = submarine_select_button_default_inner;
  destroyer_select_button.innerHTML = destroyer_select_button_default_inner;
  changeSelectedShip(ship_select_default_button);
  
  document.getElementById('person-remaining-ship-count__battleship').innerHTML = '1';
  document.getElementById('person-remaining-ship-count__cruiser').innerHTML = '2';
  document.getElementById('person-remaining-ship-count__submarine').innerHTML = '3';
  document.getElementById('person-remaining-ship-count__destroyer').innerHTML = '4';
  document.getElementById('opponent-remaining-ship-count__battleship').innerHTML = '1';
  document.getElementById('opponent-remaining-ship-count__cruiser').innerHTML = '2';
  document.getElementById('opponent-remaining-ship-count__submarine').innerHTML = '3';
  document.getElementById('opponent-remaining-ship-count__destroyer').innerHTML = '4';
  
  Array.prototype.forEach.call(ship_select_buttons, function (button) {
    button.classList.remove(ship_select_button_class_active);
    button.classList.remove(ship_select_button_class_inactive);
    button.classList.add(ship_select_button_class_default);
  });
  ship_select_default_button.classList.remove(ship_select_button_class_default);
  ship_select_default_button.classList.add(ship_select_button_class_active);
  selected_ship = ship_select_button_default;
  
  person_board.classList.remove(board_class_inactive);
  opponent_board.classList.remove(board_class_inactive);
  Array.prototype.forEach.call(person_cells, function (cell) {
    if (!cell.classList.contains(markup_cell_class)) {
      cell.innerHTML = icon_empty;
    }
  });
  Array.prototype.forEach.call(opponent_cells, function (cell) {
    if (!cell.classList.contains(markup_cell_class)) {
      cell.innerHTML = icon_empty;
    }
  });
}


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
    
    if (selected_ship_direction === direction_vertical) {
      selected_ship_direction = direction_horizontal;
    } else if (selected_ship_direction === direction_horizontal) {
      selected_ship_direction = direction_vertical;
    }
  }
}


Array.prototype.forEach.call(ship_select_buttons, function (element) {
  element.addEventListener('click', function () {
    changeSelectedShip(element);
  });
});

function changeSelectedShip(ship) {
  let current_ships_count = parseInt(ship.innerHTML.split(ship_count_sep)[1]);
  let current_ship = ship.innerHTML.split(ship_count_sep)[0];
  if (current_ships_count >= 0 && !ship.classList.contains(ship_select_button_class_inactive)) {
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


Array.prototype.forEach.call(person_cells, function (element) {
  if (!element.classList.contains(markup_cell_class)) {
    element.addEventListener('click', function () {
      handlePersonBoardClick(element);
    });
    
    element.addEventListener('mouseover', function () {
      handlePersonCellHover(element);
    });
    
    element.addEventListener('mouseout', function () {
      handlePersonCellUnhover();
    });
  }
});

function handlePersonBoardClick(cell) {
  const person_board_click_response = $.post('/person_cell_clicked', {
    username: username.value,
    game_status: game_status.innerHTML,
    direction: selected_ship_direction,
    current_ship: selected_ship,
    cell_icon: cell.innerHTML,
    cell_id: cell.id
  });
  
  // todo if ships_remains_to_place == 0 Ready & waitForOpponentShipsPlacing
  
  person_board_click_response.done(function (data) {
    if (data['is_changed']) {
      game_status.innerHTML = data['game_status'];
      
      for (let i = 0; i < data['cells'].length; i++) {
        let current_cell = Array.from(person_cells).find(cell => cell.id === data['cells'][i]);
        current_cell.innerHTML = data['icon'];
      }
      
      if (data['returned_ship'] !== '') {
        let returned_ship = Array
          .from(ship_select_buttons)
          .find(button => button.innerHTML.split(ship_count_sep)[0] === data['returned_ship']);
        if (returned_ship.innerHTML.split(ship_count_sep)[1] === '0') {
          returned_ship.classList.remove(ship_select_button_class_inactive);
          returned_ship.classList.add(ship_select_button_class_default);
        }
        returned_ship.innerHTML = data['returned_ship'] + ship_count_sep + data['ship_count'];
        return;
      }
      
      let current_ship_select_button = Array
        .from(ship_select_buttons)
        .filter(button => button.innerHTML.split(ship_count_sep)[0] === selected_ship)[0];
      current_ship_select_button.innerHTML = selected_ship + ship_count_sep + data['ship_count'];
      if (data['ship_count'] === 0) {
        current_ship_select_button.classList.remove(ship_select_button_class_active);
        current_ship_select_button.classList.add(ship_select_button_class_inactive);
        let next_ships = Array
          .from(ship_select_buttons)
          .filter(button => button.innerHTML.split(ship_count_sep)[0] !== selected_ship
            && !button.classList.contains(ship_select_button_class_inactive));
        if (next_ships.length !== 0) {
          selected_ship = next_ships[0].innerHTML.split(ship_count_sep)[0];
          let next_ship_select_button = Array
            .from(ship_select_buttons)
            .filter(button => button.innerHTML.split(ship_count_sep)[0] === selected_ship)[0];
          next_ship_select_button.classList.remove(ship_select_button_class_default);
          next_ship_select_button.classList.add(ship_select_button_class_active);
        }
      }
      
      if (game_status.innerHTML === game_status_battle) {
        ship_placing_buttons.style.display = 'none';
        remaining_ship_panel.style.display = 'block';
      }
    }
  });
}

function handlePersonCellHover(cell) {
  const person_cell_hover_response = $.post('/person_cell_hovered', {
    game_status: game_status.innerHTML,
    current_ship: selected_ship,
    direction: selected_ship_direction,
    cell_id: cell.id
  });
  
  person_cell_hover_response.done(function (data) {
    if (data['is_changed']) {
      for (let i = 0; i < data['cells'].length; i++) {
        let current_cell = Array.from(person_cells).find(cell => cell.id === data['cells'][i]);
        hovered_cells.push(current_cell)
        current_cell.style.backgroundColor = color_cell_hovered_gray;
      }
    }
  });
}

function handlePersonCellUnhover() {
  for (let i = 0; i < hovered_cells.length; i++) {
    let current_cell = hovered_cells[i];
    current_cell.style.backgroundColor = color_white;
  }
  hovered_cells = []
}


Array.prototype.forEach.call(opponent_cells, function (element) {
  if (!element.classList.contains(markup_cell_class)) {
    element.addEventListener('click', async function () {
      if (is_opponent_ai) {
        if (game_status.innerHTML === game_status_battle) {
          handleOpponentBoardClick(element);
          await sleep(100);
          
          if (game_status.innerHTML === game_status_win) {
            showWinUI();
          }
    
          opponent_board.classList.add(board_class_inactive);
          // if (game_status.innerHTML !== game_status_win && game_status.innerHTML !== game_status_lose) {
          if (game_status.innerHTML === game_status_battle) {
            await sleep(800);
            getOpponentTurn();
            await sleep(100);
            opponent_board.classList.remove(board_class_inactive);
          }
    
          if (game_status.innerHTML === game_status_lose) {
            showLoseUI();
            showOpponentRemainingShipCells();
          }
        }
      }
      
      if (!is_opponent_ai) {
        if (game_status.innerHTML === game_status_battle) {
          handleOpponentBoardClick(element);
          await sleep(100);
          
          if (game_status.innerHTML === game_status_win) {
            showWinUI();
          }
          
          opponent_board.classList.add(board_class_inactive);
          waitForOpponentFire();
          await sleep(100);
          
          if (game_status.innerHTML === game_status_battle) {
            opponent_board.classList.remove(board_class_inactive);
          }
          
          if (game_status.innerHTML === game_status_lose) {
            showLoseUI();
            showOpponentRemainingShipCells();
          }
        }
      }
    });
  }
});

function handleOpponentBoardClick(cell) {
  const opponent_board_click_response = $.post('/opponent_cell_clicked', {
    username: username.value,
    game_status: game_status.innerHTML,
    cell_id: cell.id
  });
  
  opponent_board_click_response.done(function (data) {
    if (data['is_changed']) {
      game_status.innerHTML = data['game_status'];
      
      if (data['is_ship_destroyed'] && cell.innerHTML !== icon_destroyed) {
        changeRemainingShipCount('opponent', data['destroyed_ship'].toLowerCase(), color_green).then(r => r);
      }
      
      cell.innerHTML = data['icon'];
    }
  });
}

function waitForOpponentFire() {
  // todo toggleTurnTimer function
  
  getOpponentTurn();
  
  // todo toggleTurnTimer frunction
}

function getOpponentTurn() {
  $.ajax({
    method: 'POST',
    url: '/get_opponent_fire',
    data: {
      username: username.value,
      game_status: game_status.innerHTML
    },
    timeout: 15000,
    success: function (data) {
      if (data['is_changed']) {
        game_status.innerHTML = data['game_status'];
        let fired_cell = Array.from(person_cells).find(cell => cell.id === data['cells']);
    
        if (data['is_ship_destroyed'] && fired_cell.innerHTML !== icon_destroyed) {
          changeRemainingShipCount('person', data['destroyed_ship'].toLowerCase(), color_red).then(r => r);
        }
    
        fired_cell.innerHTML = data['icon']
        
        // todo wait for person turn for 15s
      }
    },
    error: function (jqXHR, textStatus, errorThrown) {
      console.log('get_opponent_fire: ' + jqXHR.status + ", " + textStatus + ", " + errorThrown);
      if (jqXHR.status !== 0) {
        // todo alert connection problems
        getOpponentTurn();
      }
    }
  });
}


async function changeRemainingShipCount(player, ship_name, text_color) {
  let current_ship = Array
    .from(remaining_ships)
    .find(item => item.id === `${player}${remaining_ship_count_id_template}${ship_name}`);
  
  if (current_ship.innerHTML !== '0') {
    current_ship.style.color = text_color;
    current_ship.innerHTML = (parseInt(current_ship.innerHTML) - 1).toString();
    await sleep(500);
    current_ship.style.color = color_darkgray;
  }
}

function showOpponentRemainingShipCells() {
  const opponent_remaining_ships = $.get('/get_opponent_remaining_ships');
  
  opponent_remaining_ships.done(function (data) {
    const remaining_ship_cells = data['cells'];
    
    for (let i = 0; i < remaining_ship_cells.length; i++) {
      let current_cell = Array.from(opponent_cells).find(cell => cell.id === remaining_ship_cells[i]);
      current_cell.innerHTML = data['icon'];
    }
  });
}


function showWinUI() {
  opponent_board.classList.add(board_class_inactive);
  person_board.classList.add(board_class_inactive);
  game_status.style.color = color_white;
  game_status.style.backgroundColor = color_green;
}

function showLoseUI() {
  opponent_board.classList.add(board_class_inactive);
  person_board.classList.add(board_class_inactive);
  game_status.style.color = color_white;
  game_status.style.backgroundColor = color_red;
}
