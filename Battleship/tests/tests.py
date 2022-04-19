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


class GameStatusTests(unittest.TestCase):
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
        cells = [[6, 5], [1, 9]]
        cells_id_text = game_status.person_cells_to_id_format(cells)
        expected_cell_ids = ['person-board_cell-f-5', 'person-board_cell-a-9']

        self.assertEqual(cells_id_text, expected_cell_ids)


class ShipPlacingTests(unittest.TestCase):
    def test_dont_place_ship_when_status_start(self):
        app.person.__init__()
        cell = [5, 5]
        neighbor_cell = [6, 5]
        neighbor_cell_id = game_status\
            .person_cells_to_id_format([neighbor_cell])[0]
        app.person.place_ship(cell, 'Submarine', direction_vertical)

        incorrect_game_status_response = game_status\
            .change_person_cells(icon_empty, neighbor_cell_id, 'Destroyer',
                                 direction_vertical, status_start)
        self.assertEqual(incorrect_game_status_response, {'is_changed': False})

    def test_correct_place_ship_when_status_ships_placing(self):
        app.person.__init__()
        cell = [5, 5]
        other_cell = [9, 2]
        other_cell_id = game_status.person_cells_to_id_format([other_cell])[0]
        app.person.place_ship(cell, 'Submarine', direction_vertical)

        correct_ship_place_response = game_status\
            .change_person_cells(icon_empty, other_cell_id, 'Destroyer',
                                 direction_horizontal, status_place_ships)
        self.assertEqual(correct_ship_place_response,
                         {'is_changed': True,
                          'game_status': status_place_ships,
                          'ship_count': 3, 'returned_ship': '',
                          'cells': [other_cell_id], 'cells_icon': icon_ship})

    def test_dont_place_ship_on_other_ship(self):
        app.person.__init__()
        cell = [5, 5]
        neighbor_cell = [6, 5]
        neighbor_cell_id = game_status\
            .person_cells_to_id_format([neighbor_cell])[0]
        app.person.place_ship(cell, 'Submarine', direction_vertical)

        incorrect_ship_place_response = game_status\
            .change_person_cells(icon_empty, neighbor_cell_id, 'Destroyer',
                                 direction_vertical, status_place_ships)
        self.assertEqual(incorrect_ship_place_response, {'is_changed': False})

    def test_correct_ship_remove(self):
        app.person.__init__()
        cell = [5, 5]
        cell_id = game_status.person_cells_to_id_format([cell])[0]
        app.person.place_ship(cell, 'Submarine', direction_vertical)
        submarine_cells = [[5, 5], [5, 6]]
        submarine_cells_ids = game_status\
            .person_cells_to_id_format(submarine_cells)

        remove_ship_response = game_status\
            .change_person_cells(icon_ship, cell_id, 'Destroyer',
                                 direction_horizontal, status_place_ships)
        self.assertEqual(remove_ship_response,
                         {'is_changed': True,
                          'game_status': status_place_ships,
                          'ship_count': 3, 'returned_ship': 'Submarine',
                          'cells': submarine_cells_ids,
                          'cells_icon': icon_empty})


class FireTests(unittest.TestCase):
    def test_correct_destroy(self):
        app.person.__init__()
        app.robot.__init__()
        app.person.init_opponent(app.robot)
        app.robot.place_ship([5, 5], 'Submarine', 'Vertical')
        new_game_status, cell_status = app.person.fire([5, 5])
        self.assertEqual([new_game_status, cell_status],
                         [status_battle, cell_destroyed])
        self.assertEqual(app.person.opponent_remaining_ship_cells_count, 19)
        self.assertEqual(app.robot.remaining_ship_cells_count, 19)

    def test_correct_missfire(self):
        app.person.__init__()
        app.robot.__init__()
        app.person.init_opponent(app.robot)
        app.robot.place_ship([5, 5], 'Submarine', 'Vertical')
        new_game_status, cell_status = app.person.fire([7, 5])
        self.assertEqual([new_game_status, cell_status],
                         [status_battle, cell_missfire])
        self.assertEqual(app.person.opponent_remaining_ship_cells_count, 20)
        self.assertEqual(app.robot.remaining_ship_cells_count, 20)


class GetFiredTests(unittest.TestCase):
    def test_correct_destroy(self):
        app.person.__init__()
        app.person.place_ship([5, 5], 'Submarine', 'Vertical')
        destroyed_response, one_more = app.person.get_fired([5, 5])
        self.assertEqual([destroyed_response, one_more],
                         [cell_destroyed, True])
        self.assertEqual(app.person.remaining_ship_cells_count, 19)

    def test_correct_missfire(self):
        app.person.__init__()
        app.person.place_ship([5, 5], 'Submarine', 'Vertical')
        missfire_response, one_more = app.person.get_fired([6, 5])
        self.assertEqual([missfire_response, one_more],
                         [cell_missfire, False])
        self.assertEqual(app.person.remaining_ship_cells_count, 20)

    def test_correct_fire_already_destroyed(self):
        app.person.__init__()
        app.person.place_ship([5, 5], 'Submarine', 'Vertical')
        app.person.get_fired([5, 5])
        fire_to_destroyed_response, one_more = app.person.get_fired([5, 5])
        self.assertEqual([fire_to_destroyed_response, one_more],
                         [cell_destroyed, False])
        self.assertEqual(app.person.remaining_ship_cells_count, 19)


class RobotTests(unittest.TestCase):
    def test_correct_board_init(self):
        app.robot.__init__()
        app.robot.init_board()

        robot_ships_cells = []
        for ship_name in ['Battleship', 'Cruiser', 'Submarine', 'Destroyer']:
            for ship in app.robot.ships[ship_name]:
                for cell in ship:
                    robot_ships_cells.append(cell)

        self.assertEqual(len(robot_ships_cells), 20)
        self.assertEqual(app.robot.non_placed_ships_count, 0)

        self.assertEqual(len(app.robot.ships['Battleship']), 1)
        self.assertEqual(len(app.robot.ships['Cruiser']), 2)
        self.assertEqual(len(app.robot.ships['Submarine']), 3)
        self.assertEqual(len(app.robot.ships['Destroyer']), 4)

        self.assertEqual(len(app.robot.ships['Battleship'][0]), 4)

        self.assertEqual(len(app.robot.ships['Cruiser'][0]), 3)
        self.assertEqual(len(app.robot.ships['Cruiser'][1]), 3)

        self.assertEqual(len(app.robot.ships['Submarine'][0]), 2)
        self.assertEqual(len(app.robot.ships['Submarine'][1]), 2)
        self.assertEqual(len(app.robot.ships['Submarine'][2]), 2)

        self.assertEqual(len(app.robot.ships['Destroyer'][0]), 1)
        self.assertEqual(len(app.robot.ships['Destroyer'][1]), 1)
        self.assertEqual(len(app.robot.ships['Destroyer'][2]), 1)
        self.assertEqual(len(app.robot.ships['Destroyer'][3]), 1)

    def test_random_fire(self):
        app.person.__init__()
        app.robot.__init__()
        app.robot.init_opponent(app.person)
        app.person.place_ship([5, 5], 'Submarine', direction_vertical)
        ship_cells = [[5, 5], [5, 6]]

        self.assertEqual(len(app.robot.opponent_empty_cells), 100)
        new_game_status, fired_cell, cell_status = app.robot.random_fire()
        self.assertEqual(len(app.robot.opponent_empty_cells), 99)
        self.assertEqual(new_game_status, status_battle)

        if fired_cell in ship_cells:
            self.assertEqual(cell_status, cell_destroyed)
            self.assertEqual(app.robot.opponent_remaining_ship_cells_count, 19)
            self.assertEqual(app.person.remaining_ship_cells_count, 19)
        else:
            self.assertEqual(cell_status, cell_missfire)
            self.assertEqual(app.robot.opponent_remaining_ship_cells_count, 20)
            self.assertEqual(app.person.remaining_ship_cells_count, 20)


if __name__ == '__main__':
    unittest.main()
