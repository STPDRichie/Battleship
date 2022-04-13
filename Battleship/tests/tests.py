import unittest

import app
from modules import game_status

status_start = 'Start game'
status_place_ships = 'Ships placing'
status_battle = 'Battle'
status_win = 'Win'
status_lose = 'Lose'

direction_vertical = 'Vertical'
direction_horizontal = 'Horizontal'

icon_empty = '<i class="fa-solid"></i>'
icon_ship = '<i class="fa-solid fa-circle"></i>'
icon_destroyed = '<i class="fa-solid fa-circle-xmark"></i>'
icon_missfire = '<i class="fa-regular fa-circle"></i>'

cell_empty = 'Empty'
cell_ship = 'Ship'
cell_neighbor = 'Neighbor'
cell_missfire = 'Missfire'
cell_destroyed = 'Destroyed'


class GameStatusChangingTests(unittest.TestCase):
    def test_correct_changing_status_start_to_place_ships(self):
        response = game_status.change_game_status('Start game')

        self.assertEqual(response['is_changed'], True)
        self.assertEqual(response['game_status'], 'Ships placing')
        self.assertEqual(response['game_status_remove_class'], 'game_status')
        self.assertEqual(response['game_status_add_class'],
                         'game_status-inactive')

    def test_dont_change_status_from_not_start(self):
        battle_response = game_status.change_game_status(status_battle)
        place_ships_response = game_status\
            .change_game_status(status_place_ships)
        win_response = game_status.change_game_status(status_win)
        lose_response = game_status.change_game_status(status_lose)

        self.assertEqual(battle_response['is_changed'], False)
        self.assertEqual(place_ships_response['is_changed'], False)
        self.assertEqual(win_response['is_changed'], False)
        self.assertEqual(lose_response['is_changed'], False)

    def correct_convert_cell_format(self):
        cell1, cell2 = [6, 5], [1, 9]
        cells_id_text = game_status.person_cells_to_id_format([cell1, cell2])
        expected_cell_ids = ['person-board_cell-f-5', 'person-board_cell-a-9']

        self.assertEqual(cells_id_text, expected_cell_ids)

    def test_correct_changing_person_cell(self):
        app.person.__init__()
        cell = [5, 5]
        neighbor_cell = [6, 5]
        other_cell = [9, 2]
        cell_id = game_status.person_cells_to_id_format([cell])[0]
        neighbor_cell_id = game_status\
            .person_cells_to_id_format([neighbor_cell])[0]
        other_cell_id = game_status.person_cells_to_id_format([other_cell])[0]
        app.person.place_ship(cell, 'Submarine', direction_vertical)
        submarine_cells = [[5, 5], [5, 6]]
        submarine_cells_ids = game_status\
            .person_cells_to_id_format(submarine_cells)

        incorrect_game_status_response = game_status\
            .change_person_cells(icon_empty, neighbor_cell_id, 'Destroyer',
                                 direction_vertical, status_start)
        correct_ship_place_response = game_status\
            .change_person_cells(icon_empty, other_cell_id, 'Destroyer',
                                 direction_horizontal, status_place_ships)
        incorrect_ship_place_response = game_status\
            .change_person_cells(icon_empty, neighbor_cell_id, 'Destroyer',
                                 direction_vertical, status_place_ships)
        remove_ship_response = game_status\
            .change_person_cells(icon_ship, cell_id, 'Destroyer',
                                 direction_horizontal, status_place_ships)

        self.assertEqual(incorrect_game_status_response, {'is_changed': False})
        self.assertEqual(correct_ship_place_response,
                         {'is_changed': True,
                          'game_status': status_place_ships,
                          'ship_count': 3, 'returned_ship': '',
                          'cells': [other_cell_id], 'cells_icon': icon_ship})
        self.assertEqual(incorrect_ship_place_response, {'is_changed': False})
        self.assertEqual(remove_ship_response,
                         {'is_changed': True,
                          'game_status': status_place_ships,
                          'ship_count': 3, 'returned_ship': 'Submarine',
                          'cells': submarine_cells_ids,
                          'cells_icon': icon_empty})

    def test_correct_fire_person_cell(self):
        app.person.__init__()
        app.person.place_ship([5, 5], 'Submarine', 'Vertical')
        missfire_response, one_more1 = app.person.get_fired([6, 5])
        destroyed_response, one_more2 = app.person.get_fired([5, 5])
        fire_to_destroyed_response, one_more3 = app.person.get_fired([5, 5])
        self.assertEqual([missfire_response, one_more1],
                         [cell_missfire, False])
        self.assertEqual([destroyed_response, one_more2],
                         [cell_destroyed, True])
        self.assertEqual([fire_to_destroyed_response, one_more3],
                         [cell_destroyed, False])
