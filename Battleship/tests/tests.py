import unittest

from modules import game_status


class GameStatusChangingTests(unittest.TestCase):
    def test_correct_changing_status_start_to_place_ships(self):
        response = game_status.change_game_status('Start game')

        self.assertEqual(response['is_changed'], True)
        self.assertEqual(response['game_status'], 'Ships placing')
        self.assertEqual(response['game_status_remove_class'], 'game_status')
        self.assertEqual(response['game_status_add_class'],
                         'game_status-inactive')

    def test_dont_change_status_from_not_start(self):
        battle_response = game_status.change_game_status('Battle')
        place_ships_response = game_status.change_game_status('Ships placing')
        win_response = game_status.change_game_status('Win')
        lose_response = game_status.change_game_status('Lose')

        self.assertEqual(battle_response['is_changed'], False)
        self.assertEqual(place_ships_response['is_changed'], False)
        self.assertEqual(win_response['is_changed'], False)
        self.assertEqual(lose_response['is_changed'], False)