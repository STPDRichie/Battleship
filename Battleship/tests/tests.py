from unittest import TestCase, main

import app
from modules.domain import GameStatus, CellStatus,\
    ShipName, ShipDirection, CellIcon, PlayerName
import modules.game_status as gs


def init_battle():
    app.person.__init__()
    app.robot.__init__()
    app.person.init_opponent(app.robot)
    app.robot.init_opponent(app.person)
    app.person.non_placed_ships_count = 0
    app.robot.non_placed_ships_count = 0


class ChaGameStatusTest(TestCase):
    def test_correct_changing_status_start_to_place_ships(self):
        response = gs.change_game_status(GameStatus.START.value)

        self.assertEqual(True, response['is_changed'])
        self.assertEqual(GameStatus.PLACE_SHIPS.value, response['game_status'])

    def test_dont_change_status_from_not_start(self):
        battle_response = gs.change_game_status(GameStatus.BATTLE.value)
        place_ships_response = gs\
            .change_game_status(GameStatus.PLACE_SHIPS.value)
        win_response = gs.change_game_status(GameStatus.WIN.value)
        lose_response = gs.change_game_status(GameStatus.LOSE.value)
        random_response = gs.change_game_status('blablabla')

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
        app.person.place_ship(cell, ShipName.SUBMARINE.value,
                              ShipDirection.VERTICAL.value)

        neighbor_cell_id = gs\
            .player_cells_to_id_format([neighbor_cell],
                                       PlayerName.PERSON.value)[0]
        incorrect_game_status_response = gs\
            .change_person_cells(CellIcon.EMPTY.value, neighbor_cell_id,
                                 ShipName.DESTROYER.value,
                                 ShipDirection.VERTICAL.value,
                                 GameStatus.START.value)

        self.assertEqual({'is_changed': False}, incorrect_game_status_response)

    def test_correct_ship_place(self):
        app.person.__init__()
        cell = (7, 3)
        cell_id = gs\
            .player_cells_to_id_format([cell], PlayerName.PERSON.value)[0]
        cruiser_cells = [(6, 3), (7, 3), (8, 3)]

        cruiser_cells_ids = gs\
            .player_cells_to_id_format(cruiser_cells, 'person')
        correct_ship_place_response = gs\
            .change_person_cells(CellIcon.EMPTY.value, cell_id, 'Cruiser',
                                 ShipDirection.VERTICAL.value,
                                 GameStatus.PLACE_SHIPS.value)

        self.assertEqual({'is_changed': True,
                          'game_status': GameStatus.PLACE_SHIPS.value,
                          'ship_count': 1, 'returned_ship': '',
                          'cells': cruiser_cells_ids,
                          'cells_icon': CellIcon.SHIP.value},
                         correct_ship_place_response)

    def test_dont_place_ship_on_other_ship(self):
        app.person.__init__()
        cell = (5, 5)
        neighbor_cell = (6, 5)

        neighbor_cell_id = gs\
            .player_cells_to_id_format([neighbor_cell],
                                       PlayerName.PERSON.value)[0]
        app.person.place_ship(cell, ShipName.SUBMARINE.value,
                              ShipDirection.VERTICAL.value)
        incorrect_ship_place_response = gs\
            .change_person_cells(CellIcon.EMPTY.value, neighbor_cell_id,
                                 ShipName.DESTROYER.value,
                                 ShipDirection.VERTICAL.value,
                                 GameStatus.PLACE_SHIPS.value)

        self.assertEqual({'is_changed': False}, incorrect_ship_place_response)

    def test_correct_ship_remove(self):
        app.person.__init__()
        cell = (5, 5)
        cell_id = gs\
            .player_cells_to_id_format([cell], PlayerName.PERSON.value)[0]
        app.person.place_ship(cell, ShipName.SUBMARINE.value,
                              ShipDirection.VERTICAL.value)
        submarine_cells = [(5, 5), (6, 5)]

        submarine_cells_ids = gs\
            .player_cells_to_id_format(submarine_cells,
                                       PlayerName.PERSON.value)
        remove_ship_response = gs\
            .change_person_cells(CellIcon.SHIP.value, cell_id,
                                 ShipName.DESTROYER.value,
                                 ShipDirection.HORIZONTAL.value,
                                 GameStatus.PLACE_SHIPS.value)

        self.assertEqual({'is_changed': True,
                          'game_status': GameStatus.PLACE_SHIPS.value,
                          'ship_count': 3,
                          'returned_ship': ShipName.SUBMARINE.value,
                          'cells': submarine_cells_ids,
                          'cells_icon': CellIcon.EMPTY.value},
                         remove_ship_response)


class FireTest(TestCase):
    def test_correct_destroy(self):
        app.person.__init__()
        app.robot.__init__()
        app.person.init_opponent(app.robot)
        app.robot.place_ship((5, 5), ShipName.SUBMARINE.value,
                             ShipDirection.VERTICAL.value)
        cell_status = app.person.fire((5, 5))

        self.assertEqual(CellStatus.DESTROYED.value, cell_status)
        self.assertEqual(19, app.person.opponent_remaining_ship_cells_count)
        self.assertEqual(19, app.robot.remaining_ship_cells_count)

    def test_correct_misfire(self):
        app.person.__init__()
        app.robot.__init__()
        app.person.init_opponent(app.robot)
        app.robot.place_ship((5, 5), ShipName.SUBMARINE.value,
                             ShipDirection.VERTICAL.value)
        cell_status = app.person.fire((7, 5))

        self.assertEqual(CellStatus.MISFIRE.value, cell_status)
        self.assertEqual(20, app.person.opponent_remaining_ship_cells_count)
        self.assertEqual(20, app.robot.remaining_ship_cells_count)


class GetFiredTest(TestCase):
    def test_correct_destroy(self):
        app.person.__init__()
        app.person.place_ship((5, 5), ShipName.SUBMARINE.value,
                              ShipDirection.VERTICAL.value)
        destroyed_response, one_more = app.person.get_fired((5, 5))

        self.assertEqual([CellStatus.DESTROYED.value, True],
                         [destroyed_response, one_more])
        self.assertEqual(19, app.person.remaining_ship_cells_count)

    def test_correct_misfire(self):
        app.person.__init__()
        app.person.place_ship((5, 5), ShipName.SUBMARINE.value,
                              ShipDirection.VERTICAL.value)
        misfire_response, one_more = app.person.get_fired((5, 6))

        self.assertEqual((CellStatus.MISFIRE.value, False),
                         (misfire_response, one_more))
        self.assertEqual(20, app.person.remaining_ship_cells_count)

    def test_correct_fire_already_destroyed(self):
        app.person.__init__()
        app.person.place_ship((5, 5), ShipName.SUBMARINE.value,
                              ShipDirection.VERTICAL.value)
        app.person.get_fired((5, 5))
        fire_to_destroyed_response, one_more = app.person.get_fired((5, 5))

        self.assertEqual((CellStatus.DESTROYED.value, False),
                         (fire_to_destroyed_response, one_more))
        self.assertEqual(19, app.person.remaining_ship_cells_count)


class RobotTest(TestCase):
    def test_correct_board_init(self):
        app.robot.__init__()
        app.robot.init_board()

        robot_ships_cells = []
        for ship_name in [ShipName.BATTLESHIP.value,
                          ShipName.CRUISER.value,
                          ShipName.SUBMARINE.value,
                          ShipName.DESTROYER.value]:
            for ship in app.robot.ships[ship_name]:
                for cell in ship:
                    robot_ships_cells.append(cell)

        self.assertEqual(20, len(robot_ships_cells))
        self.assertEqual(0, app.robot.non_placed_ships_count)

        self.assertEqual(1, len(app.robot.ships[ShipName.BATTLESHIP.value]))
        self.assertEqual(2, len(app.robot.ships[ShipName.CRUISER.value]))
        self.assertEqual(3, len(app.robot.ships[ShipName.SUBMARINE.value]))
        self.assertEqual(4, len(app.robot.ships[ShipName.DESTROYER.value]))

        self.assertEqual(4,
                         len(app.robot.ships[ShipName.BATTLESHIP.value][0]))

        self.assertEqual(3, len(app.robot.ships[ShipName.CRUISER.value][0]))
        self.assertEqual(3, len(app.robot.ships[ShipName.CRUISER.value][1]))

        self.assertEqual(2,
                         len(app.robot.ships[ShipName.SUBMARINE.value][0]))
        self.assertEqual(2,
                         len(app.robot.ships[ShipName.SUBMARINE.value][1]))
        self.assertEqual(2,
                         len(app.robot.ships[ShipName.SUBMARINE.value][2]))

        self.assertEqual(1,
                         len(app.robot.ships[ShipName.DESTROYER.value][0]))
        self.assertEqual(1,
                         len(app.robot.ships[ShipName.DESTROYER.value][1]))
        self.assertEqual(1,
                         len(app.robot.ships[ShipName.DESTROYER.value][2]))
        self.assertEqual(1,
                         len(app.robot.ships[ShipName.DESTROYER.value][3]))

    def test_random_fire(self):
        app.person.__init__()
        app.robot.__init__()
        app.robot.init_opponent(app.person)
        app.person.place_ship((5, 5), ShipName.SUBMARINE.value,
                              ShipDirection.VERTICAL.value)
        ship_cells = [(5, 5), (5, 6)]

        self.assertEqual(0, len(app.robot.opponent_not_empty_cells))
        fired_cell, cell_status = app.robot.random_fire()
        self.assertEqual(1, len(app.robot.opponent_not_empty_cells))

        if fired_cell in ship_cells:
            self.assertEqual(CellStatus.DESTROYED.value, cell_status)
            self.assertEqual(19, app.robot.opponent_remaining_ship_cells_count)
            self.assertEqual(19, app.person.remaining_ship_cells_count)
        else:
            self.assertEqual(CellStatus.MISFIRE.value, cell_status)
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
        person_cells_ids = gs\
            .player_cells_to_id_format(cells, PlayerName.PERSON.value)

        opponent_cells_ids = gs\
            .player_cells_to_id_format(cells, PlayerName.OPPONENT.value)

        self.assertEqual(
            ['person-board__cell_f-7', 'person-board__cell_j-2'],
            person_cells_ids)
        self.assertEqual(
            ['opponent-board__cell_f-7', 'opponent-board__cell_j-2'],
            opponent_cells_ids)

    def test_correct_convert_cell_to_computing_format(self):
        cells = ['person-board__cell_f-7', 'opponent-board__cell_j-2']

        person_cell = gs.cell_id_to_computing_format(cells[0])
        opponent_cell = gs.cell_id_to_computing_format(cells[1])

        self.assertEqual((6, 5), person_cell)
        self.assertEqual((1, 9), opponent_cell)

    def test_dont_outline_cells_when_status_not_placing_ships(self):
        cell = (5, 5)
        cell_id = gs\
            .player_cells_to_id_format([cell], PlayerName.PERSON.value)[0]

        dont_outline_cells_response = gs\
            .get_person_outline_cells(ShipName.SUBMARINE.value,
                                      ShipDirection.VERTICAL.value,
                                      cell_id, GameStatus.START.value)

        self.assertEqual({'is_changed': False}, dont_outline_cells_response)

    def test_dont_outline_cells_incorrect_to_place(self):
        cell = (0, 0)
        cell_id = gs\
            .player_cells_to_id_format([cell], PlayerName.PERSON.value)[0]

        dont_outline_cells_response = gs\
            .get_person_outline_cells(ShipName.BATTLESHIP.value,
                                      ShipDirection.VERTICAL.value,
                                      cell_id, GameStatus.PLACE_SHIPS.value)

        self.assertEqual({'is_changed': False}, dont_outline_cells_response)

    def test_correct_getting_outline_cells(self):
        cell = (5, 5)
        submarine_cells = [(5, 5), (6, 5)]
        cell_id = gs\
            .player_cells_to_id_format([cell], PlayerName.PERSON.value)[0]
        submarine_cells_ids = gs\
            .player_cells_to_id_format(submarine_cells,
                                       PlayerName.PERSON.value)

        outline_cells_response = gs\
            .get_person_outline_cells(ShipName.SUBMARINE.value,
                                      ShipDirection.VERTICAL.value,
                                      cell_id, GameStatus.PLACE_SHIPS.value)

        self.assertEqual({'is_changed': True, 'cells': submarine_cells_ids},
                         outline_cells_response)

    def test_correct_get_opponent_remaining_cells(self):
        app.robot.__init__()
        submarine_cells = [(5, 5), (6, 5)]
        remaining_cell_id = gs.player_cells_to_id_format(
            [submarine_cells[1]], PlayerName.OPPONENT.value)
        app.robot.place_ship(submarine_cells[0],
                             ShipName.SUBMARINE.value,
                             ShipDirection.VERTICAL.value)
        app.robot.get_fired(submarine_cells[0])

        response = gs.get_opponent_remaining_ship_cells()

        self.assertEqual(
            {'cells': remaining_cell_id, 'cell_icon': CellIcon.SHIP.value},
            response)


class GameStatusChangePersonCellTest(TestCase):
    def test_dont_change_person_cell_when_status_not_ships_placing(self):
        app.person.__init__()
        cell = (5, 5)
        cell_id = gs\
            .player_cells_to_id_format([cell], PlayerName.PERSON.value)[0]

        dont_change_cell_response = gs\
            .change_person_cells(CellIcon.EMPTY.value, cell_id,
                                 ShipName.DESTROYER.value,
                                 ShipDirection.VERTICAL.value,
                                 GameStatus.START.value)

        self.assertEqual({'is_changed': False}, dont_change_cell_response)

    def test_correct_change_person_cell(self):
        app.person.__init__()
        cell = (5, 5)
        submarine_cells = [(5, 5), (6, 5)]
        cell_id = gs\
            .player_cells_to_id_format([cell], PlayerName.PERSON.value)[0]
        submarine_cells_ids = gs\
            .player_cells_to_id_format(submarine_cells,
                                       PlayerName.PERSON.value)

        place_ship_response = gs\
            .change_person_cells(CellIcon.EMPTY.value, cell_id,
                                 ShipName.SUBMARINE.value,
                                 ShipDirection.VERTICAL.value,
                                 GameStatus.PLACE_SHIPS.value)

        remove_ship_response = gs\
            .change_person_cells(CellIcon.SHIP.value, cell_id,
                                 ShipName.DESTROYER.value,
                                 ShipDirection.HORIZONTAL.value,
                                 GameStatus.PLACE_SHIPS.value)

        self.assertEqual(
            {'is_changed': True,
             'game_status': GameStatus.PLACE_SHIPS.value,
             'ship_count': 2,
             'returned_ship': '',
             'cells': submarine_cells_ids,
             'cells_icon': CellIcon.SHIP.value},
            place_ship_response)
        self.assertEqual(
            {'is_changed': True,
             'game_status': GameStatus.PLACE_SHIPS.value,
             'ship_count': 3,
             'returned_ship': 'Submarine',
             'cells': submarine_cells_ids,
             'cells_icon': CellIcon.EMPTY.value},
            remove_ship_response)


class GameStatusFireTest(TestCase):
    def test_dont_fire_opponent_cell_when_status_not_battle(self):
        app.person.__init__()
        app.robot.__init__()
        cell = (5, 5)
        cell_id = gs\
            .player_cells_to_id_format([cell], PlayerName.PERSON.value)[0]

        dont_fire_response = gs\
            .fire_opponent_cell(cell_id, GameStatus.START.value)

        self.assertEqual({'is_changed': False}, dont_fire_response)

    def test_correct_fire_opponent_cell(self):
        init_battle()
        submarine_cells = [(5, 5), (6, 5)]
        other_cell = (7, 7)
        submarine_cells_ids = gs.player_cells_to_id_format(
            submarine_cells, PlayerName.OPPONENT.value)
        other_cell_id = gs.player_cells_to_id_format(
            [other_cell], PlayerName.OPPONENT.value)[0]
        app.robot.place_ship(submarine_cells[0],
                             ShipName.SUBMARINE.value,
                             ShipDirection.VERTICAL.value)

        hit_response = gs\
            .fire_opponent_cell(submarine_cells_ids[0],
                                GameStatus.BATTLE.value)
        misfire_response = gs\
            .fire_opponent_cell(other_cell_id, GameStatus.BATTLE.value)
        destroy_response = gs\
            .fire_opponent_cell(submarine_cells_ids[1],
                                GameStatus.BATTLE.value)

        self.assertEqual(
            {'is_changed': True,
             'game_status': GameStatus.BATTLE.value,
             'cell_icon': CellIcon.DESTROYED.value,
             'is_ship_destroyed': False,
             'destroyed_ship': ''},
            hit_response)
        self.assertEqual(
            {'is_changed': True,
             'game_status': GameStatus.BATTLE.value,
             'cell_icon': CellIcon.MISFIRE.value,
             'is_ship_destroyed': False,
             'destroyed_ship': ''},
            misfire_response)
        self.assertEqual(
            {'is_changed': True,
             'game_status': GameStatus.BATTLE.value,
             'cell_icon': CellIcon.DESTROYED.value,
             'is_ship_destroyed': True,
             'destroyed_ship': 'Submarine'},
            destroy_response)

    def test_dont_fire_person_cell_when_status_not_battle(self):
        dont_fire_response = gs.fire_person_cell(GameStatus.WIN.value)

        self.assertEqual({'is_changed': False}, dont_fire_response)

    def test_correct_fire_person_cell(self):
        init_battle()
        submarine_cells = [(5, 5), (6, 5)]
        app.person.place_ship(submarine_cells[0],
                              'Submarine', ShipDirection.VERTICAL.value)

        fire_response = gs.fire_person_cell(GameStatus.BATTLE.value)
        fired_cell = gs.cell_id_to_computing_format(
            fire_response['cell'])

        self.assertEqual(False, fire_response['is_ship_destroyed'])
        self.assertEqual('', fire_response['destroyed_ship'])
        if fired_cell in submarine_cells:
            self.assertEqual(CellIcon.DESTROYED.value,
                             fire_response['cell_icon'])
        else:
            self.assertEqual(CellIcon.MISFIRE.value,
                             fire_response['cell_icon'])


if __name__ == '__main__':
    main()
