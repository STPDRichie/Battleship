import time
from dataclasses import asdict

import app
from modules.app_status import get_game_if_exist, get_lobby_if_exist, \
    board_data
from modules.domain import LobbyChange, GameChange

from modules.lobby import Lobby


def host_lobby(session_key, host_name):
    lobby = Lobby(session_key, host_name)
    app.lobbies.append(lobby)
    return LobbyChange(is_lobby_exist=True, is_changed=True)


def wait_for_member_connect(session_key):
    current_lobby = get_lobby_if_exist(session_key)
    if not current_lobby:
        return LobbyChange()
    
    while True:
        time.sleep(0.5)
        if current_lobby.member_name:
            return LobbyChange(is_lobby_exist=True, is_changed=True,
                               opponent=current_lobby.member_name)


def check_is_member_in_lobby(session_key):
    while True:
        time.sleep(0.5)
        current_lobby = get_lobby_if_exist(session_key)
        if not current_lobby:
            return LobbyChange(is_lobby_exist=False, is_changed=True)
        
        if not current_lobby.member_name:
            return LobbyChange(is_lobby_exist=True, is_changed=True)


def connect_to_lobby(session_key, member_name):
    current_lobby = get_lobby_if_exist(session_key)
    
    if not current_lobby or current_lobby.member_name:
        return LobbyChange()
    
    if not current_lobby.is_game_started and \
            current_lobby.host_name != member_name:
        current_lobby.init_second_player(member_name)
        return LobbyChange(is_lobby_exist=True, is_changed=True,
                           opponent=current_lobby.host_name)
    return LobbyChange()


def wait_for_start_game(session_key):
    while True:
        time.sleep(0.5)
        current_lobby = get_lobby_if_exist(session_key)
        if not current_lobby:
            return LobbyChange(is_changed=True)
        if current_lobby.is_game_started:
            current_game = get_game_if_exist(session_key)
            return LobbyChange(is_lobby_exist=True, is_changed=True,
                               whose_turn=current_game.whose_turn,
                               opponent=current_lobby.host_name)


def leave(session_key, username):
    current_lobby = get_lobby_if_exist(session_key)
    if current_lobby:
        current_lobby.uninit_second_player()
        if current_lobby.host_name == username:
            app.lobbies.remove(current_lobby)
        
        if current_lobby.is_game_started:
            current_game = get_game_if_exist(session_key)
            if current_game:
                current_game.change_turn_player()
                turn = GameChange(is_changed=True)
                current_game.change_last_turn(turn)
                app.games.remove(current_game)
    
    return LobbyChange(is_changed=True)
