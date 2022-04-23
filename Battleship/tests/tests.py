import sys
from unittest import TestCase, main

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
icon_misfire = '<i class="fa-regular fa-circle"></i>'

cell_empty = 'Empty'
cell_ship = 'Ship'
cell_neighbor = 'Neighbor'
cell_misfire = 'Misfire'
cell_destroyed = 'Destroyed'


class GameStatusTest(TestCase):
    def test_correct_changing_status_start_to_place_ships(self):
        response = game_status.change_game_status(status_start)

        self.assertEqual(True, response['is_changed'])
        self.assertEqual(status_place_ships, response['game_status'])
        self.assertEqual('game_status', response['game_status_remove_class'])
        self.assertEqual('game_status-inactive',
                         response['game_status_add_class'])

    def test_dont_change_status_from_not_start(self):
        battle_response = game_status.change_game_status(status_battle)
        place_ships_response = game_status\
            .change_game_status(status_place_ships)
        win_response = game_status.change_game_status(status_win)
        lose_response = game_status.change_game_status(status_lose)
        random_response = game_status.change_game_status('blablabla')

        self.assertEqual(False, battle_response['is_changed'])
        self.assertEqual(False, place_ships_response['is_changed'])
        self.assertEqual(False, win_response['is_changed'])
        self.assertEqual(False, lose_response['is_changed'])
        self.assertEqual(False, random_response['is_changed'])

    def test_correct_convert_cell_format(self):
        cells = [[6, 5], [1, 9]]
        person_cells_ids = game_status\
            .player_cells_to_id_format(cells, 'person')

        opponent_cells_ids = game_status\
            .player_cells_to_id_format(cells, 'opponent')

        self.assertEqual(
            ['person-board_cell-f-7', 'person-board_cell-j-2'],
            person_cells_ids)
        self.assertEqual(
            ['opponent-board_cell-f-7', 'opponent-board_cell-j-2'],
            opponent_cells_ids)


class ShipPlacingTest(TestCase):
    def test_dont_place_ship_when_status_start(self):
        app.person.__init__()
        cell = [5, 5]
        neighbor_cell = [6, 5]
        app.person.place_ship(cell, 'Submarine', direction_vertical)

        neighbor_cell_id = game_status\
            .player_cells_to_id_format([neighbor_cell], 'person')[0]
        incorrect_game_status_response = game_status\
            .change_person_cells(icon_empty, neighbor_cell_id, 'Destroyer',
                                 direction_vertical, status_start)

        self.assertEqual({'is_changed': False}, incorrect_game_status_response)

    def test_correct_ship_place(self):
        app.person.__init__()
        cell = [7, 3]
        cell_id = game_status.player_cells_to_id_format([cell], 'person')[0]
        cruiser_cells = [[6, 3], [7, 3], [8, 3]]

        cruiser_cells_ids = game_status\
            .player_cells_to_id_format(cruiser_cells, 'person')
        correct_ship_place_response = game_status\
            .change_person_cells(icon_empty, cell_id, 'Cruiser',
                                 direction_vertical, status_place_ships)

        self.assertEqual({'is_changed': True,
                          'game_status': status_place_ships,
                          'ship_count': 1, 'returned_ship': '',
                          'cells': cruiser_cells_ids,
                          'cells_icon': icon_ship},
                         correct_ship_place_response)

    def test_dont_place_ship_on_other_ship(self):
        app.person.__init__()
        cell = [5, 5]
        neighbor_cell = [6, 5]

        neighbor_cell_id = game_status\
            .player_cells_to_id_format([neighbor_cell], 'person')[0]
        app.person.place_ship(cell, 'Submarine', direction_vertical)
        incorrect_ship_place_response = game_status\
            .change_person_cells(icon_empty, neighbor_cell_id, 'Destroyer',
                                 direction_vertical, status_place_ships)

        self.assertEqual({'is_changed': False}, incorrect_ship_place_response)

    def test_correct_ship_remove(self):
        app.person.__init__()
        cell = [5, 5]
        cell_id = game_status.player_cells_to_id_format([cell], 'person')[0]
        app.person.place_ship(cell, 'Submarine', direction_vertical)
        submarine_cells = [[5, 5], [6, 5]]

        submarine_cells_ids = game_status\
            .player_cells_to_id_format(submarine_cells, 'person')
        remove_ship_response = game_status\
            .change_person_cells(icon_ship, cell_id, 'Destroyer',
                                 direction_horizontal, status_place_ships)

        self.assertEqual({'is_changed': True,
                          'game_status': status_place_ships,
                          'ship_count': 3, 'returned_ship': 'Submarine',
                          'cells': submarine_cells_ids,
                          'cells_icon': icon_empty},
                         remove_ship_response)


class FireTest(TestCase):
    def test_correct_destroy(self):
        app.person.__init__()
        app.robot.__init__()
        app.person.init_opponent(app.robot)
        app.robot.place_ship([5, 5], 'Submarine', direction_vertical)
        cell_status = app.person.fire([5, 5])

        self.assertEqual(cell_destroyed, cell_status)
        self.assertEqual(19, app.person.opponent_remaining_ship_cells_count)
        self.assertEqual(19, app.robot.remaining_ship_cells_count)

    def test_correct_misfire(self):
        app.person.__init__()
        app.robot.__init__()
        app.person.init_opponent(app.robot)
        app.robot.place_ship([5, 5], 'Submarine', direction_vertical)
        cell_status = app.person.fire([7, 5])

        self.assertEqual(cell_misfire, cell_status)
        self.assertEqual(20, app.person.opponent_remaining_ship_cells_count)
        self.assertEqual(20, app.robot.remaining_ship_cells_count)


class GetFiredTest(TestCase):
    def test_correct_destroy(self):
        app.person.__init__()
        app.person.place_ship([5, 5], 'Submarine', direction_vertical)
        destroyed_response, one_more = app.person.get_fired([5, 5])

        self.assertEqual([cell_destroyed, True],
                         [destroyed_response, one_more])
        self.assertEqual(19, app.person.remaining_ship_cells_count)

    def test_correct_misfire(self):
        app.person.__init__()
        app.person.place_ship([5, 5], 'Submarine', direction_vertical)
        misfire_response, one_more = app.person.get_fired([5, 6])

        self.assertEqual([cell_misfire, False], [misfire_response, one_more])
        self.assertEqual(20, app.person.remaining_ship_cells_count)

    def test_correct_fire_already_destroyed(self):
        app.person.__init__()
        app.person.place_ship([5, 5], 'Submarine', direction_vertical)
        app.person.get_fired([5, 5])
        fire_to_destroyed_response, one_more = app.person.get_fired([5, 5])

        self.assertEqual([cell_destroyed, False],
                         [fire_to_destroyed_response, one_more])
        self.assertEqual(19, app.person.remaining_ship_cells_count)


class RobotTest(TestCase):
    def test_correct_board_init(self):
        app.robot.__init__()
        app.robot.init_board()

        robot_ships_cells = []
        for ship_name in ['Battleship', 'Cruiser', 'Submarine', 'Destroyer']:
            for ship in app.robot.ships[ship_name]:
                for cell in ship:
                    robot_ships_cells.append(cell)

        self.assertEqual(20, len(robot_ships_cells))
        self.assertEqual(0, app.robot.non_placed_ships_count)

        self.assertEqual(1, len(app.robot.ships['Battleship']))
        self.assertEqual(2, len(app.robot.ships['Cruiser']))
        self.assertEqual(3, len(app.robot.ships['Submarine']))
        self.assertEqual(4, len(app.robot.ships['Destroyer']))

        self.assertEqual(4, len(app.robot.ships['Battleship'][0]))

        self.assertEqual(3, len(app.robot.ships['Cruiser'][0]))
        self.assertEqual(3, len(app.robot.ships['Cruiser'][1]))

        self.assertEqual(2, len(app.robot.ships['Submarine'][0]))
        self.assertEqual(2, len(app.robot.ships['Submarine'][1]))
        self.assertEqual(2, len(app.robot.ships['Submarine'][2]))

        self.assertEqual(1, len(app.robot.ships['Destroyer'][0]))
        self.assertEqual(1, len(app.robot.ships['Destroyer'][1]))
        self.assertEqual(1, len(app.robot.ships['Destroyer'][2]))
        self.assertEqual(1, len(app.robot.ships['Destroyer'][3]))

    def test_random_fire(self):
        app.person.__init__()
        app.robot.__init__()
        app.robot.init_opponent(app.person)
        app.person.place_ship([5, 5], 'Submarine', direction_vertical)
        ship_cells = [[5, 5], [5, 6]]

        self.assertEqual(100, len(app.robot.opponent_empty_cells))
        fired_cell, cell_status = app.robot.random_fire()
        self.assertEqual(99, len(app.robot.opponent_empty_cells))

        if fired_cell in ship_cells:
            self.assertEqual(cell_destroyed, cell_status)
            self.assertEqual(19, app.robot.opponent_remaining_ship_cells_count)
            self.assertEqual(19, app.person.remaining_ship_cells_count)
        else:
            self.assertEqual(cell_misfire, cell_status)
            self.assertEqual(20, app.robot.opponent_remaining_ship_cells_count)
            self.assertEqual(20, app.person.remaining_ship_cells_count)


if __name__ == '__main__':
    main()
