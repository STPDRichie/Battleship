from unittest import TestCase, main

import app
import modules.lobby_status as l_s
import modules.game_status as g_s
import modules.app_status as a_s
from modules.domain import *

from modules.lobby import Lobby
from modules.game import Game

from modules.player import Player, get_ship_direction
from modules.robot import Robot


_session_key = 1
_player1_name = 'Host'
_player2_name = 'Member'


def _init_singleplayer_game():
    l_s.host_lobby(_session_key, _player1_name)
    start_response = g_s.start_game(_session_key, GameStatus.START.value)
    return start_response


def _init_multiplayer_game():
    l_s.host_lobby(_session_key, _player1_name)
    l_s.connect_to_lobby(_session_key, _player2_name)
    start_response = g_s.start_game(_session_key, GameStatus.START.value)
    return start_response


class LobbyTest(TestCase):
    def test_correct_host_lobby(self):
        response = l_s.host_lobby(_session_key, _player1_name)
        self.assertEqual(LobbyChange(is_changed=True, is_lobby_exist=True),
                         response)
        self.assertEqual(1, len(app.lobbies))


class ChangeGameStatusTest(TestCase):
    pass


class ShipPlacingTest(TestCase):
    pass


class FireTest(TestCase):
    pass


class GetFiredTest(TestCase):
    pass


class RobotTest(TestCase):
    pass


class GameStatusTest(TestCase):
    pass


class GameStatusChangePersonCellTest(TestCase):
    pass


class GameStatusFireTest(TestCase):
    pass


if __name__ == '__main__':
    main()
