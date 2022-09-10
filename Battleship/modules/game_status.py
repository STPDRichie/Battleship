import time
from dataclasses import replace

import app
from modules.app_status import *
from modules.domain import GameStatus, PlayerName, CellStatus, CellIcon, \
    GameChange, BoardData, REQUEST_UPDATE_RATE

from modules.game import Game
from modules.robot import Robot


def wait_for_restart_game(session_key) -> GameChange:
    while True:
        time.sleep(REQUEST_UPDATE_RATE)
        current_game = get_game_if_exist(session_key)
        if not current_game:
            return GameChange(is_changed=True)
        if current_game.last_turn and \
                current_game.last_turn.is_game_restarted:
            return GameChange(is_lobby_exist=True, is_changed=True,
                              is_game_restarted=True,
                              whose_turn=current_game.whose_turn)


def start_game(session_key, current_status) -> GameChange:
    if current_status != GameStatus.START.value:
        return GameChange()
    
    current_lobby = get_lobby_if_exist(session_key)
    if not current_lobby:
        return GameChange()
    
    init_response = init_game(current_lobby, board_data)
    return init_response


def init_game(lobby: Lobby, board: BoardData) -> GameChange:
    lobby.is_game_started = True
    current_game = get_game_if_exist(lobby.session_key)
    
    if current_game:
        current_game.__init__(lobby, board)
    else:
        current_game = Game(lobby, board)
        app.games.append(current_game)
    return GameChange(is_changed=True,
                      whose_turn=current_game.whose_turn,
                      game_status=GameStatus.PLACE_SHIPS.value)


def restart_game(session_key) -> GameChange:
    current_game = get_game_if_exist(session_key)
    
    if current_game and current_game.lobby:
        current_game.__init__(current_game.lobby, current_game.board_data)
        turn = GameChange(is_lobby_exist=True, is_changed=True,
                          is_game_restarted=True,
                          whose_turn=current_game.whose_turn)
        current_game.change_last_turn(turn)
        return turn
    return GameChange()


def wait_for_opponent_ready(session_key, username) -> GameChange:
    while True:
        time.sleep(REQUEST_UPDATE_RATE)
        current_game = get_game_if_exist(session_key)
        if not current_game:
            return GameChange(is_changed=True)
        
        if current_game.last_turn and \
                current_game.last_turn.is_game_restarted and \
                current_game.lobby.host_name != username:
            turn = current_game.last_turn
            current_game.change_last_turn(None)
            return turn
        
        # if not current_game.lobby.member_name and \
        #         not isinstance(current_game.player2, Robot):
        #     return GameChange(is_changed=True)
        
        current_player = get_current_player(current_game, username)
        is_person_ready = current_player.is_ready_for_battle()
        if current_player.opponent.is_ready_for_battle():
            return GameChange(is_lobby_exist=True, is_changed=True,
                              is_person_ready_for_battle=is_person_ready,
                              is_opponent_ready_for_battle=True,
                              whose_turn=current_game.whose_turn)


def get_ship_outline_cells(session_key, username,
                           ship, ship_direction, cell_id) -> GameChange:
    current_game = get_game_if_exist(session_key)
    if not current_game:
        return GameChange()
    
    current_player = get_current_player(current_game, username)
    
    cell = convert_cell_id_to_computing_format(cell_id)
    cells = current_player.get_ship_cells(cell, ship, ship_direction)
    
    current_ship_range = current_game.board_data.get_ships_ranges()[ship]
    ship_length = abs(current_ship_range[0]) + current_ship_range[1] + 1
    if len(cells) != ship_length:
        return GameChange()
    
    cells_ids = convert_player_cells_to_id(cells, PlayerName.PERSON.value)
    
    return GameChange(is_changed=True, cells=cells_ids)


def change_person_cells(session_key, username, cell_icon, cell_id, ship,
                        ship_direction, current_status) -> GameChange:
    current_game, current_player, response_if_incorrect = \
        get_game_and_player_if_correct(session_key, username,
                                       current_status,
                                       GameStatus.PLACE_SHIPS.value)
    if response_if_incorrect:
        return response_if_incorrect
    
    cell = convert_cell_id_to_computing_format(cell_id)
    
    ship_count, returned_ship, cells_ids, new_icon = \
        get_change_player_cell_info(current_player, cell, cell_icon,
                                    ship, ship_direction)
    if not cells_ids:
        return GameChange()
    
    new_game_status, is_person_ready, is_opponent_ready = \
        get_game_status_info(current_player)
    
    if new_game_status == GameStatus.BATTLE.value:
        current_game.is_battle_started = True
    
    return GameChange(is_changed=True, game_status=new_game_status,
                      whose_turn=current_game.whose_turn,
                      ship_count=ship_count, returned_ship=returned_ship,
                      cells=cells_ids, icon=new_icon,
                      is_person_ready_for_battle=is_person_ready,
                      is_opponent_ready_for_battle=is_opponent_ready)


def fire_opponent_cell(session_key, username,
                       cell_id, current_status) -> GameChange:
    current_game, current_player, response_if_incorrect = \
        get_game_and_player_if_correct(session_key, username,
                                       current_status,
                                       GameStatus.BATTLE.value)
    if response_if_incorrect:
        return response_if_incorrect
    
    cell = convert_cell_id_to_computing_format(cell_id)
    fired_cell_status = current_player.fire(cell)
    new_game_status = current_player.check_game_status()
    
    new_icon, is_ship_destroyed, destroyed_ship = \
        get_fire_info(cell, fired_cell_status, current_player.opponent)
    
    return update_game_and_get_last_turn(current_game, new_game_status,
                                         [cell_id], new_icon,
                                         is_ship_destroyed, destroyed_ship)


def get_opponent_turn(session_key, username, current_status) -> GameChange:
    if (current_status == GameStatus.WIN.value or
            current_status == GameStatus.LOSE.value):
        return wait_for_restart_game(session_key)
    
    current_game = get_game_if_correct(session_key, current_status,
                                       GameStatus.BATTLE.value)
    if not current_game:
        return GameChange(is_changed=True)
    
    current_player = get_current_player(current_game, username)
    if isinstance(current_player.opponent, Robot):
        return get_robot_fire(current_game)
    
    while True:
        time.sleep(REQUEST_UPDATE_RATE)
        last_turn = current_game.last_turn
        if last_turn and last_turn.is_game_restarted and \
                current_game.lobby.host_name != username:
            turn = last_turn
            current_game.change_last_turn(None)
            return turn
        if last_turn and last_turn.whose_turn == username:
            fired_cell = None
            if last_turn.cells:
                fired_cell = last_turn.cells[0]
            response_turn = replace(
                last_turn,
                cells=cells_to_other_player_id_format([fired_cell]))
            return response_turn


def get_robot_fire(current_game) -> GameChange:
    fired_cell, fired_cell_status = current_game.player2.random_fire()
    new_game_status = current_game.player2.check_game_status()
    fired_cell_id = \
        convert_player_cells_to_id([fired_cell], PlayerName.PERSON.value)[0]
    
    new_icon, is_ship_destroyed, destroyed_ship = \
        get_fire_info(fired_cell, fired_cell_status, current_game.player1)
    
    return update_game_and_get_last_turn(current_game, new_game_status,
                                         [fired_cell_id], new_icon,
                                         is_ship_destroyed, destroyed_ship)


def get_opponent_remaining_ship_cells(session_key, username) -> GameChange:
    current_game = get_game_if_exist(session_key)
    if not current_game:
        return GameChange(is_changed=True)
    
    current_player = get_current_player(current_game, username)
    
    remaining_cells = current_player.opponent.get_remaining_ship_cells()
    cells_ids = convert_player_cells_to_id(remaining_cells,
                                           PlayerName.OPPONENT.value)
    return GameChange(is_lobby_exist=True, is_changed=True,
                      cells=cells_ids, icon=CellIcon.SHIP.value)


def update_game_and_get_last_turn(current_game, game_status,
                                  cells, icon, is_ship_destroyed,
                                  destroyed_ship) -> GameChange:
    current_game.change_turn_player()
    turn = GameChange(is_lobby_exist=True, is_changed=True,
                      whose_turn=current_game.whose_turn,
                      game_status=game_status,
                      cells=cells,
                      icon=icon, is_ship_destroyed=is_ship_destroyed,
                      destroyed_ship=destroyed_ship)
    current_game.change_last_turn(turn)
    return turn


def get_game_if_correct(session_key, current_status, required_status):
    if current_status != required_status or not session_key:
        return None
    
    current_game = get_game_if_exist(session_key)
    if not current_game:
        return None
    
    return current_game


def get_current_player(current_game, username):
    if current_game.lobby.host_name == username:
        return current_game.player1
    return current_game.player2


def get_game_and_player_if_correct(session_key, username,
                                   current_status, required_status):
    current_game = get_game_if_correct(session_key, current_status,
                                       required_status)
    if not current_game:
        return None, None, GameChange()
    
    if current_game.last_turn and \
            current_game.last_turn.is_game_restarted and \
            current_game.lobby.host_name != username:
        turn = current_game.last_turn
        current_game.change_last_turn(None)
        current_player = get_current_player(current_game, username)
        return current_game, current_player, turn
    
    current_player = get_current_player(current_game, username)
    
    return current_game, current_player, None


def get_change_player_cell_info(current_player, cell, cell_icon,
                                ship, ship_direction):
    returned_ship = ''
    if cell_icon == CellIcon.EMPTY.value:
        ship_cells = current_player.place_ship(cell, ship, ship_direction)
        if not ship_cells:
            return None, None, None, None
        ship_count = current_player.get_remains_to_place_ship_count(ship)
        new_icon = CellIcon.SHIP.value
    elif cell_icon == CellIcon.SHIP.value:
        returned_ship = current_player.get_ship_name(cell)
        ship_cells = current_player.uninit_and_get_ship_cells(cell)
        ship_count = current_player \
            .get_remains_to_place_ship_count(returned_ship)
        new_icon = CellIcon.EMPTY.value
    else:
        return None, None, None, None
    
    cells_ids = convert_player_cells_to_id(ship_cells,
                                           PlayerName.PERSON.value)
    
    return ship_count, returned_ship, cells_ids, new_icon


def get_game_status_info(current_player):
    new_game_status = current_player.check_game_status()
    is_person_ready = current_player.is_ready_for_battle()
    is_opponent_ready = current_player.opponent.is_ready_for_battle()
    
    return new_game_status, is_person_ready, is_opponent_ready


def get_fire_info(fired_cell, fired_cell_status, opponent):
    new_icon = CellIcon.MISFIRE.value
    if fired_cell_status == CellStatus.DESTROYED.value:
        new_icon = CellIcon.DESTROYED.value
    
    is_ship_destroyed = opponent.is_ship_destroyed(fired_cell)
    destroyed_ship = ''
    if is_ship_destroyed:
        destroyed_ship = opponent.get_ship_name(fired_cell)
    
    return new_icon, is_ship_destroyed, destroyed_ship
