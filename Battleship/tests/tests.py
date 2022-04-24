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


def init_battle():
    app.person.__init__()
    app.robot.__init__()
    app.person.init_opponent(app.robot)
    app.robot.init_opponent(app.person)
    app.person.non_placed_ships_count = 0
    app.robot.non_placed_ships_count = 0


class ChangeGameStatusTest(TestCase):
    def test_correct_changing_status_start_to_place_ships(self):
        response = game_status.change_game_status(status_start)

        self.assertEqual(True, response['is_changed'])
        self.assertEqual(status_place_ships, response['game_status'])

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


class ShipPlacingTest(TestCase):
    def test_dont_place_ship_when_status_start(self):
        app.person.__init__()
        cell = (5, 5)
        neighbor_cell = (6, 5)
        app.person.place_ship(cell, 'Submarine', direction_vertical)

        neighbor_cell_id = game_status\
            .player_cells_to_id_format([neighbor_cell], 'person')[0]
        incorrect_game_status_response = game_status\
            .change_person_cells(icon_empty, neighbor_cell_id, 'Destroyer',
                                 direction_vertical, status_start)

        self.assertEqual({'is_changed': False}, incorrect_game_status_response)

    def test_correct_ship_place(self):
        app.person.__init__()
        cell = (7, 3)
        cell_id = game_status.player_cells_to_id_format([cell], 'person')[0]
        cruiser_cells = [(6, 3), (7, 3), (8, 3)]

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
        cell = (5, 5)
        neighbor_cell = (6, 5)

        neighbor_cell_id = game_status\
            .player_cells_to_id_format([neighbor_cell], 'person')[0]
        app.person.place_ship(cell, 'Submarine', direction_vertical)
        incorrect_ship_place_response = game_status\
            .change_person_cells(icon_empty, neighbor_cell_id, 'Destroyer',
                                 direction_vertical, status_place_ships)

        self.assertEqual({'is_changed': False}, incorrect_ship_place_response)

    def test_correct_ship_remove(self):
        app.person.__init__()
        cell = (5, 5)
        cell_id = game_status.player_cells_to_id_format([cell], 'person')[0]
        app.person.place_ship(cell, 'Submarine', direction_vertical)
        submarine_cells = [(5, 5), (6, 5)]

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
        app.robot.place_ship((5, 5), 'Submarine', direction_vertical)
        cell_status = app.person.fire((5, 5))

        self.assertEqual(cell_destroyed, cell_status)
        self.assertEqual(19, app.person.opponent_remaining_ship_cells_count)
        self.assertEqual(19, app.robot.remaining_ship_cells_count)

    def test_correct_misfire(self):
        app.person.__init__()
        app.robot.__init__()
        app.person.init_opponent(app.robot)
        app.robot.place_ship((5, 5), 'Submarine', direction_vertical)
        cell_status = app.person.fire((7, 5))

        self.assertEqual(cell_misfire, cell_status)
        self.assertEqual(20, app.person.opponent_remaining_ship_cells_count)
        self.assertEqual(20, app.robot.remaining_ship_cells_count)


class GetFiredTest(TestCase):
    def test_correct_destroy(self):
        app.person.__init__()
        app.person.place_ship((5, 5), 'Submarine', direction_vertical)
        destroyed_response, one_more = app.person.get_fired((5, 5))

        self.assertEqual([cell_destroyed, True],
                         [destroyed_response, one_more])
        self.assertEqual(19, app.person.remaining_ship_cells_count)

    def test_correct_misfire(self):
        app.person.__init__()
        app.person.place_ship((5, 5), 'Submarine', direction_vertical)
        misfire_response, one_more = app.person.get_fired((5, 6))

        self.assertEqual((cell_misfire, False), (misfire_response, one_more))
        self.assertEqual(20, app.person.remaining_ship_cells_count)

    def test_correct_fire_already_destroyed(self):
        app.person.__init__()
        app.person.place_ship((5, 5), 'Submarine', direction_vertical)
        app.person.get_fired((5, 5))
        fire_to_destroyed_response, one_more = app.person.get_fired((5, 5))

        self.assertEqual((cell_destroyed, False),
                         (fire_to_destroyed_response, one_more))
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
        app.person.place_ship((5, 5), 'Submarine', direction_vertical)
        ship_cells = [(5, 5), (5, 6)]

        self.assertEqual(0, len(app.robot.opponent_not_empty_cells))
        fired_cell, cell_status = app.robot.random_fire()
        self.assertEqual(1, len(app.robot.opponent_not_empty_cells))

        if fired_cell in ship_cells:
            self.assertEqual(cell_destroyed, cell_status)
            self.assertEqual(19, app.robot.opponent_remaining_ship_cells_count)
            self.assertEqual(19, app.person.remaining_ship_cells_count)
        else:
            self.assertEqual(cell_misfire, cell_status)
            self.assertEqual(20, app.robot.opponent_remaining_ship_cells_count)
            self.assertEqual(20, app.person.remaining_ship_cells_count)

    def test_correct_update_cells_to_fire(self):
        app.robot.__init__()
        cell = (5, 5)
        next_cell = (6, 5)
        app.robot.last_destroyed_cell = cell
        app.robot.next_cells_to_fire = [(4, 5), (5, 4), (5, 6), (6, 5)]

        app.robot.update_cells_to_fire_by_destroyed(next_cell)

        self.assertEqual([(4, 5), (6, 5), (7, 5)],
                         app.robot.next_cells_to_fire)

    def test_correct_get_empty_cells_from_neighbors(self):
        app.robot.__init__()
        app.robot.opponent_not_empty_cells = [(7, 2), (5, 4), (5, 5)]
        neighbors = [(4, 5), (5, 4), (5, 6), (6, 5)]

        empty_cells = app.robot.get_empty_cells_from_neighbors(neighbors)

        self.assertEqual([(4, 5), (5, 6), (6, 5)], empty_cells)


class GameStatusTest(TestCase):
    def test_correct_convert_cell_to_id_format(self):
        cells = [(6, 5), (1, 9)]
        person_cells_ids = game_status\
            .player_cells_to_id_format(cells, 'person')

        opponent_cells_ids = game_status\
            .player_cells_to_id_format(cells, 'opponent')

        self.assertEqual(
            ['person-board__cell_f-7', 'person-board__cell_j-2'],
            person_cells_ids)
        self.assertEqual(
            ['opponent-board__cell_f-7', 'opponent-board__cell_j-2'],
            opponent_cells_ids)

    def test_correct_convert_cell_to_computing_format(self):
        cells = ['person-board__cell_f-7', 'opponent-board__cell_j-2']

        person_cell = game_status.cell_id_to_computing_format(cells[0])
        opponent_cell = game_status.cell_id_to_computing_format(cells[1])

        self.assertEqual((6, 5), person_cell)
        self.assertEqual((1, 9), opponent_cell)

    def test_dont_outline_cells_when_status_not_placing_ships(self):
        cell = (5, 5)
        cell_id = game_status.player_cells_to_id_format([cell], 'person')[0]

        dont_outline_cells_response = game_status.get_person_outline_cells(
            'Submarine', direction_vertical, cell_id, status_start)

        self.assertEqual({'is_changed': False}, dont_outline_cells_response)

    def test_dont_outline_cells_incorrect_to_place(self):
        cell = (0, 0)
        cell_id = game_status.player_cells_to_id_format([cell], 'person')[0]

        dont_outline_cells_response = game_status.get_person_outline_cells(
            'Battleship', direction_vertical, cell_id, status_place_ships)

        self.assertEqual({'is_changed': False}, dont_outline_cells_response)

    def test_correct_getting_outline_cells(self):
        cell = (5, 5)
        submarine_cells = [(5, 5), (6, 5)]
        cell_id = game_status.player_cells_to_id_format([cell], 'person')[0]
        submarine_cells_ids = game_status\
            .player_cells_to_id_format(submarine_cells, 'person')

        outline_cells_response = game_status.get_person_outline_cells(
            'Submarine', direction_vertical, cell_id, status_place_ships)

        self.assertEqual({'is_changed': True, 'cells': submarine_cells_ids},
                         outline_cells_response)

    def test_correct_get_opponent_remaining_cells(self):
        app.robot.__init__()
        submarine_cells = [(5, 5), (6, 5)]
        remaining_cell_id = game_status.player_cells_to_id_format(
            [submarine_cells[1]], 'opponent')
        app.robot.place_ship(submarine_cells[0],
                             'Submarine', direction_vertical)
        app.robot.get_fired(submarine_cells[0])

        response = game_status.get_opponent_remaining_ship_cells()

        self.assertEqual(
            {'cells': remaining_cell_id, 'cell_icon': icon_ship}, response)


class GameStatusChangePersonCellTest(TestCase):
    def test_dont_change_person_cell_when_status_not_ships_placing(self):
        app.person.__init__()
        cell = (5, 5)
        cell_id = game_status.player_cells_to_id_format([cell], 'person')[0]

        dont_change_cell_response = game_status.change_person_cells(
            icon_empty, cell_id, 'Destroyer', direction_vertical, status_start)

        self.assertEqual({'is_changed': False}, dont_change_cell_response)

    def test_correct_change_person_cell(self):
        app.person.__init__()
        cell = (5, 5)
        submarine_cells = [(5, 5), (6, 5)]
        cell_id = game_status.player_cells_to_id_format([cell], 'person')[0]
        submarine_cells_ids = game_status\
            .player_cells_to_id_format(submarine_cells, 'person')

        place_ship_response = game_status.change_person_cells(
            icon_empty, cell_id, 'Submarine',
            direction_vertical, status_place_ships)

        remove_ship_response = game_status.change_person_cells(
            icon_ship, cell_id, 'Destroyer',
            direction_horizontal, status_place_ships)

        self.assertEqual(
            {'is_changed': True,
             'game_status': status_place_ships,
             'ship_count': 2,
             'returned_ship': '',
             'cells': submarine_cells_ids,
             'cells_icon': icon_ship},
            place_ship_response)
        self.assertEqual(
            {'is_changed': True,
             'game_status': status_place_ships,
             'ship_count': 3,
             'returned_ship': 'Submarine',
             'cells': submarine_cells_ids,
             'cells_icon': icon_empty},
            remove_ship_response)


class GameStatusFireTest(TestCase):
    def test_dont_fire_opponent_cell_when_status_not_battle(self):
        app.person.__init__()
        app.robot.__init__()
        cell = (5, 5)
        cell_id = game_status.player_cells_to_id_format([cell], 'person')[0]

        dont_fire_response = game_status\
            .fire_opponent_cell(cell_id, status_start)

        self.assertEqual({'is_changed': False}, dont_fire_response)

    def test_correct_fire_opponent_cell(self):
        init_battle()
        submarine_cells = [(5, 5), (6, 5)]
        other_cell = (7, 7)
        submarine_cells_ids = game_status.player_cells_to_id_format(
            submarine_cells, 'opponent')
        other_cell_id = game_status.player_cells_to_id_format(
            [other_cell], 'opponent')[0]
        app.robot.place_ship(submarine_cells[0],
                             'Submarine', direction_vertical)

        hit_response = game_status.fire_opponent_cell(submarine_cells_ids[0],
                                                      status_battle)
        misfire_response = game_status.fire_opponent_cell(other_cell_id,
                                                          status_battle)
        destroy_response = game_status.fire_opponent_cell(
            submarine_cells_ids[1], status_battle)

        self.assertEqual(
            {'is_changed': True,
             'game_status': status_battle,
             'cell_icon': icon_destroyed,
             'is_ship_destroyed': False,
             'destroyed_ship': ''},
            hit_response)
        self.assertEqual(
            {'is_changed': True,
             'game_status': status_battle,
             'cell_icon': icon_misfire,
             'is_ship_destroyed': False,
             'destroyed_ship': ''},
            misfire_response)
        self.assertEqual(
            {'is_changed': True,
             'game_status': status_battle,
             'cell_icon': icon_destroyed,
             'is_ship_destroyed': True,
             'destroyed_ship': 'Submarine'},
            destroy_response)

    def test_dont_fire_person_cell_when_status_not_battle(self):
        dont_fire_response = game_status.fire_person_cell(status_win)

        self.assertEqual({'is_changed': False}, dont_fire_response)

    def test_correct_fire_person_cell(self):
        init_battle()
        submarine_cells = [(5, 5), (6, 5)]
        app.person.place_ship(submarine_cells[0],
                              'Submarine', direction_vertical)

        fire_response = game_status.fire_person_cell(status_battle)
        fired_cell = game_status.cell_id_to_computing_format(
            fire_response['cell'])

        self.assertEqual(False, fire_response['is_ship_destroyed'])
        self.assertEqual('', fire_response['destroyed_ship'])
        if fired_cell in submarine_cells:
            self.assertEqual(icon_destroyed, fire_response['cell_icon'])
        else:
            self.assertEqual(icon_misfire, fire_response['cell_icon'])


if __name__ == '__main__':
    main()
