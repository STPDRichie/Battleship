import time
from dataclasses import dataclass, field, asdict

import app
from modules.game import Game
from modules.lobby import Lobby
from modules.domain import GameStatus, PlayerName, CellStatus, CellIcon
from modules.player import get_ship_cells, ships_ranges

column_numbers_and_letters = {
    'a': 1, 1: 'a',
    'b': 2, 2: 'b',
    'c': 3, 3: 'c',
    'd': 4, 4: 'd',
    'e': 5, 5: 'e',
    'f': 6, 6: 'f',
    'g': 7, 7: 'g',
    'h': 8, 8: 'h',
    'i': 9, 9: 'i',
    'j': 10, 10: 'j'
}


def host_lobby(session_key, host_name):
    lobby = Lobby(session_key, host_name)
    app.lobbies.append(lobby)
    return asdict(LobbyChange(is_lobby_exist=True, is_changed=True))


def wait_for_member_connect(session_key):
    current_lobby = next((lobby for lobby in app.lobbies
                          if lobby.session_key == session_key), None)
    if not current_lobby:
        return asdict(LobbyChange())
    
    while True:
        time.sleep(0.5)
        if current_lobby.member_name:
            return asdict(LobbyChange(is_lobby_exist=True, is_changed=True,
                                      opponent=current_lobby.member_name))


def check_for_member_connection(session_key):
    current_lobby = next((lobby for lobby in app.lobbies
                          if lobby.session_key == session_key), None)
    while True:
        time.sleep(0.5)
        if not current_lobby:
            return asdict(LobbyChange())
        if not current_lobby.member_name:
            return asdict(LobbyChange(is_lobby_exist=True,
                                      is_changed=True, opponent=''))


def connect_to_lobby(session_key, member_name):
    current_lobby = next((lobby for lobby in app.lobbies
                          if lobby.session_key == session_key), None)
    
    if not current_lobby or current_lobby.member_name:
        return asdict(LobbyChange())
    
    if not current_lobby.is_game_started and \
            current_lobby.host_name != member_name:
        current_lobby.init_second_player(member_name)
        return asdict(LobbyChange(is_lobby_exist=True, is_changed=True,
                                  opponent=current_lobby.host_name))
    return asdict(LobbyChange())


def check_for_start_game(session_key):
    while True:
        time.sleep(0.5)
        current_lobby = next((lobby for lobby in app.lobbies
                              if lobby.session_key == session_key), None)
        
        if not current_lobby:
            return asdict(LobbyChange(is_changed=True, opponent=''))
        if current_lobby.is_game_started:
            return asdict(LobbyChange(is_lobby_exist=True, is_changed=True,
                                      opponent=current_lobby.host_name))


def wait_for_opponent_ready_for_battle(session_key):
    while True:
        time.sleep(0.5)
        current_lobby = next((lobby for lobby in app.lobbies
                              if lobby.session_key == session_key), None)

        if not current_lobby or not current_lobby.member_name:
            return asdict(GameChange(is_lobby_exist=False, is_changed=True))
        if current_lobby.is_game_started:
            return asdict(GameChange(is_lobby_exist=True, is_changed=True,
                                     is_opponent_ready_for_battle=True))


def leave(session_key, username):
    current_lobby = next((lobby for lobby in app.lobbies
                          if lobby.session_key == session_key), None)
    if current_lobby:
        current_lobby.uninit_second_player()
        if username == current_lobby.host_name:
            app.lobbies.remove(current_lobby)
    
    return asdict(LobbyChange(is_changed=True))


def start_game(session_key, current_status):
    if current_status != GameStatus.START.value:
        return asdict(GameChange())
    
    current_lobby = next((lobby for lobby in app.lobbies
                          if lobby.session_key == session_key), None)
    if not current_lobby:
        return asdict(GameChange())
    
    init_response = init_game(current_lobby)
    return asdict(init_response)


def init_game(lobby):
    lobby.is_game_started = True
    current_game = next((g for g in app.games if g.lobby == lobby), None)
    
    if current_game:
        current_game.__init__(lobby)
    else:
        current_game = Game(lobby)
        app.games.append(current_game)
    return GameChange(is_changed=True,
                      next_turn_player_name=current_game.next_turn_player_name,
                      game_status=GameStatus.PLACE_SHIPS.value)


def restart_game(session_key):
    current_game = next((g for g in app.games
                         if g.lobby.session_key == session_key), None)
    
    if current_game:
        current_game.__init__(current_game.lobby)
        return asdict(
            GameChange(is_changed=True,
                       next_turn_player_name=current_game.next_turn))
    return asdict(GameChange())


def get_person_outline_cells(ship, ship_direction,
                             cell_id, current_status):
    if current_status != GameStatus.PLACE_SHIPS.value:
        return asdict(GameChange())
    
    cell = cell_id_to_computing_format(cell_id)
    cells = get_ship_cells(cell, ship, ship_direction)
    
    ship_length = abs(ships_ranges[ship][0]) + ships_ranges[ship][1] + 1
    if len(cells) != ship_length:
        return asdict(GameChange())
    
    cells_ids = player_cells_to_id_format(cells, PlayerName.PERSON.value)
    
    return asdict(GameChange(is_changed=True, cells=cells_ids))


def change_person_cells(session_key, username, cell_icon, cell_id, ship,
                        ship_direction, current_status):
    current_game = get_game_if_correct(session_key, current_status,
                                       GameStatus.PLACE_SHIPS.value)
    if not current_game:
        return asdict(GameChange())
    
    current_player = get_current_player(current_game, username)
    if not current_player:
        return asdict(GameChange())
    
    cell = cell_id_to_computing_format(cell_id)
    
    if cell_icon == CellIcon.EMPTY.value:
        returned_ship = ''
        ship_cells = current_player.place_ship(cell, ship, ship_direction)
        if not ship_cells:
            return asdict(GameChange())
        new_game_status = current_player.check_game_status()
        is_person_ready = current_player.is_ready_for_battle()
        is_opponent_ready = current_player.opponent.is_ready_for_battle()
        cells_ids = player_cells_to_id_format(ship_cells,
                                              PlayerName.PERSON.value)
        ship_count = current_player.get_remains_to_place_ship_count(ship)
        new_icon = CellIcon.SHIP.value
    elif cell_icon == CellIcon.SHIP.value:
        returned_ship = current_player.get_ship_name(cell)
        ship_cells = current_player.uninit_and_get_ship_cells(cell)
        new_game_status = current_player.check_game_status()
        is_person_ready = current_player.is_ready_for_battle()
        is_opponent_ready = current_player.opponent.is_ready_for_battle()
        cells_ids = player_cells_to_id_format(ship_cells,
                                              PlayerName.PERSON.value)
        ship_count = current_player \
            .get_remains_to_place_ship_count(returned_ship)
        new_icon = CellIcon.EMPTY.value
    else:
        return asdict(GameChange())
    
    if new_game_status == GameStatus.BATTLE.value:
        current_game.is_battle_started = True
    
    return asdict(
        GameChange(is_changed=True, game_status=new_game_status,
                   ship_count=ship_count, returned_ship=returned_ship,
                   cells=cells_ids, icon=new_icon,
                   is_person_ready_for_battle=is_person_ready,
                   is_opponent_ready_for_battle=is_opponent_ready))


def fire_opponent_cell(session_key, username, cell_id, current_status):
    current_game = get_game_if_correct(session_key, current_status,
                                       GameStatus.BATTLE.value)
    if not current_game:
        return asdict(GameChange())
    
    current_player = get_current_player(current_game, username)
    opponent_name = get_opponent_name(current_game, username)
    
    if not current_player:
        return asdict(GameChange())
    
    cell = cell_id_to_computing_format(cell_id)
    fired_cell_status = current_player.fire(cell)
    new_game_status = current_player.check_game_status()
    
    new_icon, is_ship_destroyed, destroyed_ship = \
        get_fire_info(fired_cell, fired_cell_status, current_player.opponent)
    
    turn = GameChange(is_changed=True, next_turn_player_name=opponent_name,
                      game_status=new_game_status,
                      icon=new_icon, is_ship_destroyed=is_ship_destroyed,
                      destroyed_ship=destroyed_ship)
    current_game.last_turn = turn
    current_game.next_turn_player_name = opponent_name
    
    return asdict(turn)


def get_robot_fire(session_key, current_status):
    current_game = get_game_if_correct(session_key, current_status,
                                       GameStatus.BATTLE.value)
    if not current_game:
        return asdict(GameChange())
    
    fired_cell, fired_cell_status = current_game.player2.random_fire()
    new_game_status = current_game.player1.check_game_status()
    fired_cell_id = \
        player_cells_to_id_format([fired_cell], PlayerName.PERSON.value)[0]

    new_icon, is_ship_destroyed, destroyed_ship = \
        get_fire_info(fired_cell, fired_cell_status, current_game.player1)
    
    return asdict(
        GameChange(is_changed=True, game_status=new_game_status,
                   cells=[fired_cell_id], icon=new_icon,
                   is_ship_destroyed=is_ship_destroyed,
                   destroyed_ship=destroyed_ship))


def get_opponent_remaining_ship_cells(session_key):
    current_game = next((g for g in app.games
                         if g.lobby.session_key == session_key), None)
    
    remaining_cells = current_game.player2.get_remaining_ship_cells()
    cells_ids = player_cells_to_id_format(remaining_cells,
                                          PlayerName.OPPONENT.value)
    return asdict(GameChange(cells=cells_ids, icon=CellIcon.SHIP.value))


def get_game_if_correct(session_key, current_status, required_status):
    if current_status != required_status or not session_key:
        return None
    
    current_game = next((g for g in app.games
                         if g.lobby.session_key == session_key), None)
    if not current_game:
        return None
    
    return current_game


def get_fire_info(fired_cell, fired_cell_status, opponent):
    new_icon = CellIcon.MISFIRE.value
    if fired_cell_status == CellStatus.DESTROYED.value:
        new_icon = CellIcon.DESTROYED.value
    
    is_ship_destroyed = opponent.is_ship_destroyed(fired_cell)
    destroyed_ship = ''
    if is_ship_destroyed:
        destroyed_ship = opponent.get_ship_name(fired_cell)
    
    return new_icon, is_ship_destroyed, destroyed_ship


def get_current_player(current_game, username):
    if username == current_game.lobby.host_name:
        return current_game.player1
    return current_game.player2


def get_opponent_name(current_game, username):
    if username == current_game.lobby.host_name:
        return current_game.lobby.member_name
    return current_game.lobby.host_name


def cell_id_to_computing_format(cell_id):
    column_row = cell_id.split('_')[-1].split('-')
    column = int(column_numbers_and_letters[column_row[0]]) - 1
    row = int(column_row[1]) - 1
    return row, column


def player_cells_to_id_format(cells, player):
    cells_ids = []
    for cell in cells:
        cells_ids.append(
            f'{player}-board__cell_' +
            f'{column_numbers_and_letters[cell[1] + 1]}-{cell[0] + 1}')
    
    return cells_ids


def cells_to_other_player_id_format(cells_ids):
    cells = []
    for cell_id in cells_ids:
        cells.append(cell_id_to_computing_format(cell_id))
    
    if cells_ids[0].split('-')[0] == PlayerName.PERSON.value:
        return player_cells_to_id_format(cells, PlayerName.PERSON.value)
    return player_cells_to_id_format(cells, PlayerName.OPPONENT.value)


@dataclass(frozen=True)
class GameChange:
    is_lobby_exist: bool = False
    is_changed: bool = False
    next_turn_player_name: str = None
    game_status: str = GameStatus.START.value
    cells: list = field(default_factory=list)
    icon: str = CellIcon.EMPTY.value
    is_ship_destroyed: bool = False
    destroyed_ship: str = ''
    ship_count: int = 0
    returned_ship: str = ''
    is_person_ready_for_battle: bool = False
    is_opponent_ready_for_battle: bool = False


@dataclass(frozen=True)
class LobbyChange:
    is_lobby_exist: bool = False
    is_changed: bool = False
    opponent: str = None
