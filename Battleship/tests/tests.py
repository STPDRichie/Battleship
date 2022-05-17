from unittest import TestCase, main
from dataclasses import asdict

import app
import modules.lobby_status as l_s
import modules.game_status as g_s
import modules.app_status as a_s
from modules.domain import *

from modules.lobby import Lobby
from modules.game import Game

from modules.player import Player, get_ship_direction
from modules.robot import Robot

_session1_key = 1
_session2_key = 2
_player1_name = 'Host'
_player2_name = 'Member'
_player3_name = 'ThirdWheel'
_robot_name = 'Robot'

_player_cells = [(4, 3), (8, 2)]
_person_cells_ids = ['person-board__cell_d-5', 'person-board__cell_c-9']
_opponent_cells_ids = ['opponent-board__cell_d-5', 'opponent-board__cell_c-9']


def _init_singleplayer_lobby(session_key):
    l_s.host_lobby(session_key, _player1_name)


def _init_multiplayer_lobby(session_key):
    l_s.host_lobby(session_key, _player1_name)
    l_s.connect_to_lobby(session_key, _player2_name)


def _init_singleplayer_game(session_key):
    l_s.host_lobby(session_key, _player1_name)
    g_s.start_game(session_key, GameStatus.START.value)


def _init_multiplayer_game(session_key):
    l_s.host_lobby(session_key, _player1_name)
    l_s.connect_to_lobby(session_key, _player2_name)
    g_s.start_game(session_key, GameStatus.START.value)


class AppStatusTest(TestCase):
    def test_get_lobby_if_exist(self):
        app.reset_app_components()
        lobby = Lobby(_session1_key, _player1_name, _player2_name)
        app.lobbies.append(lobby)
        current_lobby = a_s.get_lobby_if_exist(_session1_key)
        
        self.assertEqual(1, len(app.lobbies))
        self.assertIsNot(None, current_lobby)
        self.assertEqual(_player1_name, current_lobby.host_name)
        self.assertEqual(_player2_name, current_lobby.member_name)
    
    def test_try_get_lobby_if_doesnt_exist(self):
        app.reset_app_components()
        current_lobby = a_s.get_lobby_if_exist(_session1_key)
        
        self.assertEqual(0, len(app.lobbies))
        self.assertIs(None, current_lobby)
    
    def test_get_game_if_exist(self):
        app.reset_app_components()
        lobby = Lobby(_session1_key, _player1_name, _player2_name)
        app.lobbies.append(lobby)
        game = Game(lobby, a_s.board_data)
        app.games.append(game)
        current_game = a_s.get_game_if_exist(_session1_key)
        
        self.assertEqual(1, len(app.games))
        self.assertIsNot(None, current_game)
        self.assertEqual(lobby, current_game.lobby)
        self.assertEqual(_player1_name, current_game.lobby.host_name)
        self.assertEqual(_player2_name, current_game.lobby.member_name)
    
    def test_try_get_game_if_doesnt_exist(self):
        app.reset_app_components()
        current_game = a_s.get_game_if_exist(_session1_key)
        
        self.assertEqual(0, len(app.games))
        self.assertIs(None, current_game)
    
    def test_convert_cell_id_to_computing_format(self):
        cell1 = a_s.convert_cell_id_to_computing_format(_person_cells_ids[0])
        cell2 = a_s.convert_cell_id_to_computing_format(_opponent_cells_ids[1])
        
        self.assertEqual(_player_cells[0], cell1)
        self.assertEqual(_player_cells[1], cell2)
    
    def test_convert_cells_to_id_format(self):
        cells_ids = a_s.convert_player_cells_to_id(_player_cells,
                                                   PlayerName.PERSON.value)
        
        self.assertEqual(_person_cells_ids, cells_ids)
    
    def test_convert_cells_ids_to_other_player_cell_id_format(self):
        other_player_cells_ids_1 = \
            a_s.cells_to_other_player_id_format(_person_cells_ids)
        other_player_cells_ids_2 = \
            a_s.cells_to_other_player_id_format(_opponent_cells_ids)
        
        self.assertEqual(_opponent_cells_ids, other_player_cells_ids_1)
        self.assertEqual(_person_cells_ids, other_player_cells_ids_2)
    
    def test_convert_empty_list_to_other_player_cell_id_format(self):
        other_player_cells_ids = a_s.cells_to_other_player_id_format([])
        
        self.assertIs(None, other_player_cells_ids)


class LobbyTest(TestCase):
    def test_host_lobby(self):
        app.reset_app_components()
        response = l_s.host_lobby(_session1_key, _player1_name)
        current_lobby = a_s.get_lobby_if_exist(_session1_key)
        
        self.assertEqual(LobbyChange(is_changed=True, is_lobby_exist=True),
                         response)
        self.assertEqual(current_lobby.host_name, _player1_name)
        self.assertEqual(1, len(app.lobbies))
    
    def test_connect_to_lobby(self):
        app.reset_app_components()
        l_s.host_lobby(_session1_key, _player1_name)
        connect_response = l_s.connect_to_lobby(_session1_key, _player2_name)
        current_lobby = a_s.get_lobby_if_exist(_session1_key)
        
        self.assertEqual(LobbyChange(is_lobby_exist=True, is_changed=True,
                                     opponent=_player1_name),
                         connect_response)
        self.assertEqual(_player2_name, current_lobby.member_name)
    
    def test_dont_connect_if_lobby_doesnt_exist(self):
        app.reset_app_components()
        connect_response = l_s.connect_to_lobby(_session1_key, _player2_name)
        current_lobby = a_s.get_lobby_if_exist(_session1_key)
        
        self.assertEqual(LobbyChange(), connect_response)
        self.assertIs(None, current_lobby)
    
    def test_dont_connect_if_lobby_has_member(self):
        app.reset_app_components()
        _init_multiplayer_lobby(_session1_key)
        connect_response = l_s.connect_to_lobby(_session1_key, _player3_name)
        current_lobby = a_s.get_lobby_if_exist(_session1_key)
        
        self.assertEqual(LobbyChange(), connect_response)
        self.assertEqual(_player2_name, current_lobby.member_name)
    
    def test_dont_connect_if_same_usernames(self):
        app.reset_app_components()
        _init_singleplayer_lobby(_session1_key)
        connect_response = l_s.connect_to_lobby(_session1_key, _player1_name)
        current_lobby = a_s.get_lobby_if_exist(_session1_key)
        
        self.assertEqual(LobbyChange(), connect_response)
        self.assertIsNot(None, current_lobby)
        self.assertIs(None, current_lobby.member_name)
    
    def test_dont_connect_if_game_is_started(self):
        app.reset_app_components()
        _init_singleplayer_game(_session1_key)
        current_lobby = a_s.get_lobby_if_exist(_session1_key)
        connect_response = l_s.connect_to_lobby(_session1_key, _player2_name)
        
        self.assertEqual(LobbyChange(), connect_response)
        self.assertIsNot(None, current_lobby)
        self.assertIs(None, current_lobby.member_name)
        self.assertTrue(current_lobby.is_game_started)
    
    def test_member_leave(self):
        app.reset_app_components()
        _init_multiplayer_lobby(_session1_key)
        current_lobby = a_s.get_lobby_if_exist(_session1_key)
        member_name_before_leave = current_lobby.member_name
        leave_response = l_s.leave(_session1_key, _player2_name)
        member_name_after_leave = current_lobby.member_name
        
        self.assertIsNot(None, member_name_before_leave)
        self.assertTrue(leave_response.is_changed)
        self.assertIs(None, member_name_after_leave)
    
    def test_host_leave(self):
        app.reset_app_components()
        _init_multiplayer_lobby(_session1_key)
        lobbies_count_before_leave = len(app.lobbies)
        leave_response = l_s.leave(_session1_key, _player1_name)
        lobbies_count_after_leave = len(app.lobbies)
        
        self.assertEqual(1, lobbies_count_before_leave)
        self.assertTrue(leave_response.is_changed)
        self.assertEqual(0, lobbies_count_after_leave)
    
    def test_wait_for_member_connect(self):
        app.reset_app_components()
        l_s.host_lobby(_session1_key, _player1_name)
        l_s.connect_to_lobby(_session1_key, _player2_name)
        wait_response = l_s.wait_for_member_connect(_session1_key)
        current_lobby = a_s.get_lobby_if_exist(_session1_key)
        
        self.assertTrue(wait_response.is_changed)
        self.assertTrue(wait_response.is_lobby_exist)
        self.assertEqual(_player2_name, current_lobby.member_name)
    
    def test_dont_wait_for_member_connect_if_lobby_doesnt_exist(self):
        app.reset_app_components()
        wait_response = l_s.wait_for_member_connect(_session1_key)
        
        self.assertFalse(wait_response.is_changed)
        self.assertFalse(wait_response.is_lobby_exist)
    
    def test_check_for_member_in_non_existent_lobby(self):
        app.reset_app_components()
        check_response = l_s.check_is_member_in_lobby(_session1_key)
        
        self.assertTrue(check_response.is_changed)
        self.assertFalse(check_response.is_lobby_exist)
    
    def test_check_for_member_in_lobby_if_he_doesnt_exist(self):
        app.reset_app_components()
        _init_singleplayer_lobby(_session1_key)
        check_response = l_s.check_is_member_in_lobby(_session1_key)
        current_lobby = a_s.get_lobby_if_exist(_session1_key)
        
        self.assertTrue(check_response.is_changed)
        self.assertTrue(check_response.is_lobby_exist)
        self.assertIs(None, current_lobby.member_name)
    
    def test_wait_for_start_game(self):
        app.reset_app_components()
        _init_multiplayer_game(_session1_key)
        wait_response = l_s.wait_for_start_game(_session1_key)
        current_lobby = a_s.get_lobby_if_exist(_session1_key)
        
        self.assertTrue(wait_response.is_changed)
        self.assertTrue(wait_response.is_lobby_exist)
        self.assertTrue(current_lobby.is_game_started)
    
    def test_dont_wait_for_start_game_if_lobby_doesnt_exist(self):
        app.reset_app_components()
        wait_response = l_s.wait_for_start_game(_session1_key)
        
        self.assertTrue(wait_response.is_changed)
        self.assertFalse(wait_response.is_lobby_exist)


class GameStatusTest(TestCase):
    def test_change_game_status_to_ships_placing_on_start_game(self):
        app.reset_app_components()
        l_s.host_lobby(_session1_key, _player1_name)
        start_response = g_s.start_game(_session1_key, GameStatus.START.value)
        
        self.assertTrue(start_response.is_changed)
        self.assertEqual(GameStatus.PLACE_SHIPS.value,
                         start_response.game_status)
    
    def test_init_game_if_already_exist(self):
        app.reset_app_components()
        _init_multiplayer_game(_session1_key)
        current_game = a_s.get_game_if_exist(_session1_key)
        current_game.change_last_turn(GameChange())
        last_turn_before_init = current_game.last_turn
        init_response = g_s.init_game(current_game.lobby, a_s.board_data)
        last_turn_after_init = current_game.last_turn
        
        self.assertEqual(GameChange(), last_turn_before_init)
        self.assertTrue(init_response.is_changed)
        self.assertIs(None, last_turn_after_init)
    
    def test_leave_if_game_started(self):
        app.reset_app_components()
        _init_multiplayer_game(_session1_key)
        games_count_before_leave = len(app.games)
        current_game = a_s.get_game_if_exist(_session1_key)
        leave_response = l_s.leave(_session1_key, _player2_name)
        games_count_after_leave = len(app.games)
        
        self.assertEqual(1, games_count_before_leave)
        self.assertIsNot(None, current_game)
        self.assertTrue(leave_response.is_changed)
        self.assertFalse(leave_response.is_lobby_exist)
        self.assertEqual(0, games_count_after_leave)


class StartGameTest(TestCase):
    def test_start_singleplayer_game(self):
        app.reset_app_components()
        l_s.host_lobby(_session1_key, _player1_name)
        start_response = g_s.start_game(_session1_key, GameStatus.START.value)
        current_game = a_s.get_game_if_exist(_session1_key)
        
        self.assertTrue(current_game.lobby.is_game_started)
        self.assertEqual(GameChange(is_changed=True,
                                    whose_turn=current_game.whose_turn,
                                    game_status=GameStatus.PLACE_SHIPS.value),
                         start_response)
        self.assertIsInstance(current_game.player2, Robot)
    
    def test_start_multiplayer_game(self):
        app.reset_app_components()
        l_s.host_lobby(_session1_key, _player1_name)
        l_s.connect_to_lobby(_session1_key, _player2_name)
        start_response = g_s.start_game(_session1_key, GameStatus.START.value)
        current_game = a_s.get_game_if_exist(_session1_key)
        
        self.assertTrue(current_game.lobby.is_game_started)
        self.assertEqual(GameChange(is_changed=True,
                                    whose_turn=current_game.whose_turn,
                                    game_status=GameStatus.PLACE_SHIPS.value),
                         start_response)
        self.assertEqual(_player2_name, current_game.lobby.member_name)
        self.assertIsInstance(current_game.player2, Player)
        
    def test_dont_start_game_if_lobby_doesnt_exist(self):
        app.reset_app_components()
        start_response = g_s.start_game(_session1_key, GameStatus.START.value)
        current_game = a_s.get_game_if_exist(_session1_key)
        
        self.assertIs(None, current_game)
        self.assertFalse(start_response.is_changed)
    
    def test_dont_start_game_if_status_is_not_start(self):
        app.reset_app_components()
        l_s.host_lobby(_session1_key, _player1_name)
        start_response = g_s.start_game(_session1_key,
                                        GameStatus.PLACE_SHIPS.value)
        
        self.assertFalse(start_response.is_changed)
    
    def test_change_last_turn_after_game_restart(self):
        app.reset_app_components()
        _init_multiplayer_game(_session1_key)
        current_game = a_s.get_game_if_exist(_session1_key)
        current_game.change_last_turn(
            GameChange(is_lobby_exist=True, is_changed=True,
                       is_game_restarted=True))
        last_turn_before_wait = current_game.last_turn
        wait_response = g_s.\
            wait_for_opponent_ready(_session1_key, _player2_name)
        
        self.assertIsNot(None, last_turn_before_wait)
        self.assertTrue(wait_response.is_changed)
        self.assertTrue(wait_response.is_game_restarted)
        self.assertIs(None, current_game.last_turn)


class RestartGameTest(TestCase):
    def test_restart_game(self):
        app.reset_app_components()
        l_s.host_lobby(_session1_key, _player1_name)
        g_s.start_game(_session1_key, GameStatus.START.value)
        current_game = a_s.get_game_if_exist(_session1_key)
        last_turn_before_restart = current_game.last_turn
        g_s.restart_game(_session1_key)
        last_turn_after_restart = current_game.last_turn
        
        self.assertIs(None, last_turn_before_restart)
        self.assertIsNot(None, last_turn_after_restart)
        self.assertTrue(last_turn_after_restart.is_game_restarted)
    
    def test_dont_restart_game_if_game_doesnt_exist(self):
        app.reset_app_components()
        restart_response = g_s.restart_game(_session1_key)
        
        self.assertFalse(restart_response.is_game_restarted)
        self.assertFalse(restart_response.is_lobby_exist)
    
    def test_wait_for_restart_game(self):
        app.reset_app_components()
        _init_multiplayer_game(_session1_key)
        current_game = a_s.get_game_if_exist(_session1_key)
        current_game.change_last_turn(
            GameChange(is_lobby_exist=True, is_changed=True,
                       is_game_restarted=True))
        wait_response = g_s.wait_for_restart_game(_session1_key)
        
        self.assertTrue(wait_response.is_changed)
        self.assertTrue(wait_response.is_game_restarted)
    
    def test_dont_wait_for_restart_if_game_doesnt_exist(self):
        app.reset_app_components()
        wait_response = g_s.wait_for_restart_game(_session1_key)
        
        self.assertTrue(wait_response.is_changed)
        self.assertFalse(wait_response.is_lobby_exist)


class ReadyTest(TestCase):
    def test_wait_for_opponent_ready_for_battle(self):
        app.reset_app_components()
        _init_multiplayer_game(_session1_key)
        current_game = a_s.get_game_if_exist(_session1_key)
        current_game.player1.non_placed_ships_count = 0
        current_game.player2.non_placed_ships_count = 0
        wait_response = g_s\
            .wait_for_opponent_ready(_session1_key, _player1_name)
        
        self.assertTrue(wait_response.is_lobby_exist)
        self.assertTrue(wait_response.is_changed)
        self.assertTrue(wait_response.is_person_ready_for_battle)
        self.assertTrue(wait_response.is_opponent_ready_for_battle)
    
    def test_dont_wait_for_opponent_ready_if_game_doesnt_exist(self):
        app.reset_app_components()
        wait_response = g_s\
            .wait_for_opponent_ready(_session1_key, _player1_name)
        
        self.assertTrue(wait_response.is_changed)
        self.assertFalse(wait_response.is_lobby_exist)
    
    def test_dont_wait_for_opponent_ready_if_he_left(self):
        app.reset_app_components()
        _init_multiplayer_game(_session1_key)
        l_s.leave(_session1_key, _player2_name)
        wait_response = g_s\
            .wait_for_opponent_ready(_session1_key, _player1_name)
        
        self.assertTrue(wait_response.is_changed)
        self.assertFalse(wait_response.is_lobby_exist)


class ShipsPlacingTest(TestCase):
    def test_get_outline_cells(self):
        app.reset_app_components()
        _init_multiplayer_game(_session1_key)
        get_response = g_s\
            .get_ship_outline_cells(_session1_key, _player1_name,
                                    ShipName.DESTROYER.value,
                                    ShipDirection.VERTICAL.value,
                                    _person_cells_ids[0])
        
        self.assertTrue(get_response.is_changed)
        self.assertEqual([_person_cells_ids[0]], get_response.cells)
    
    def test_dont_get_outline_cells_if_is_incorrect_place(self):
        app.reset_app_components()
        _init_multiplayer_game(_session1_key)
        get_response = g_s\
            .get_ship_outline_cells(_session1_key, _player1_name,
                                    ShipName.BATTLESHIP.value,
                                    ShipDirection.VERTICAL.value,
                                    _person_cells_ids[1])
        
        self.assertFalse(get_response.is_changed)
    
    def test_dont_get_outline_cells_if_game_doesnt_exist(self):
        app.reset_app_components()
        get_response = g_s\
            .get_ship_outline_cells(_session1_key, _player1_name,
                                    ShipName.DESTROYER.value,
                                    ShipDirection.VERTICAL.value,
                                    _person_cells_ids[0])
        
        self.assertFalse(get_response.is_changed)
    
    def test_place_ship(self):
        pass
    
    def test_dont_place_ship_if_is_incorrect_place(self):
        app.reset_app_components()
        _init_multiplayer_game(_session1_key)
        place_response = g_s\
            .change_person_cells(_session1_key, _player1_name,
                                 CellIcon.EMPTY.value, _person_cells_ids[0],
                                 ShipName.DESTROYER.value,
                                 ShipDirection.VERTICAL.value,
                                 GameStatus.PLACE_SHIPS.value)
    
    def test_dont_place_ship_if_game_status_not_ships_placing(self):
        app.reset_app_components()
        _init_multiplayer_lobby(_session1_key)
        place_response = g_s\
            .change_person_cells(_session1_key, _player1_name,
                                 CellIcon.EMPTY.value, _person_cells_ids[0],
                                 ShipName.DESTROYER.value,
                                 ShipDirection.VERTICAL.value,
                                 GameStatus.START.value)
        
        self.assertFalse(place_response.is_changed)


class FireTest(TestCase):
    pass


class GetFiredTest(TestCase):
    pass


class RobotTest(TestCase):
    pass


if __name__ == '__main__':
    main()
