from dataclasses import dataclass

import app
from modules.domain import GameStatus, PlayerName, CellStatus, CellIcon
from modules.player import get_ship_cells, ships_ranges


column_numbers_and_letters = {
    'a': 1, 1: 'a',
    'b': 2, 2: 'b',
    'c': 3, 3: 'c',
    'd': 4, 4: 'd',
    'e': 5, 5: 'e',
    'f': 6, 6: 'f',
    'g': 7, 7: 'g',
    'h': 8, 8: 'h',
    'i': 9, 9: 'i',
    'j': 10, 10: 'j'
}


def change_game_status(current_status):
    if current_status != GameStatus.START.value:
        return Response().to_dict()

    game_status = GameStatus.PLACE_SHIPS.value
    init_game()

    return Response(is_changed=True, game_status=game_status).to_dict()


def init_game():
    app.person.__init__()
    app.robot.__init__()
    app.person.init_opponent(app.robot)
    app.robot.init_opponent(app.person)
    app.robot.init_board()
    return Response(is_changed=True).to_dict()


def get_person_outline_cells(ship, ship_direction,
                             cell_id, current_status):
    if current_status != GameStatus.PLACE_SHIPS.value:
        return Response().to_dict()

    cell = cell_id_to_computing_format(cell_id)
    cells = get_ship_cells(cell, ship, ship_direction)

    ship_length = abs(ships_ranges[ship][0]) + ships_ranges[ship][1] + 1
    if len(cells) != ship_length:
        return Response().to_dict()

    cells_ids = player_cells_to_id_format(cells, PlayerName.PERSON.value)

    return Response(is_changed=True, cells=cells_ids).to_dict()


def change_person_cells(cell_icon, cell_id, ship,
                        ship_direction, current_status):
    if current_status != GameStatus.PLACE_SHIPS.value:
        return Response().to_dict()

    cell = cell_id_to_computing_format(cell_id)

    if cell_icon == CellIcon.EMPTY.value:
        returned_ship = ''
        ship_cells = app.person.place_ship(cell, ship, ship_direction)
        if not ship_cells:
            return Response().to_dict()
        new_game_status = app.person.check_game_status()
        cells_ids = player_cells_to_id_format(ship_cells,
                                              PlayerName.PERSON.value)
        ship_count = app.person.get_ship_count(ship)
        new_icon = CellIcon.SHIP.value
    elif cell_icon == CellIcon.SHIP.value:
        returned_ship = app.person.get_ship(cell)
        ship_cells = app.person.get_ship_cells(cell)
        new_game_status = app.person.check_game_status()
        cells_ids = player_cells_to_id_format(ship_cells,
                                              PlayerName.PERSON.value)
        ship_count = app.person.get_ship_count(returned_ship)
        new_icon = CellIcon.EMPTY.value
    else:
        return Response().to_dict()

    return Response(is_changed=True, game_status=new_game_status,
                    ship_count=ship_count, returned_ship=returned_ship,
                    cells=cells_ids, icon=new_icon).to_dict()


def fire_opponent_cell(cell_id, current_status):
    if current_status != GameStatus.BATTLE.value:
        return Response().to_dict()

    cell = cell_id_to_computing_format(cell_id)
    fired_cell_status = app.person.fire(cell)
    new_game_status = app.person.check_game_status()

    if fired_cell_status == CellStatus.DESTROYED.value:
        new_icon = CellIcon.DESTROYED.value
        is_ship_destroyed = app.robot.is_ship_destroyed(cell)
    else:
        new_icon = CellIcon.MISFIRE.value
        is_ship_destroyed = False

    destroyed_ship = ''
    if is_ship_destroyed:
        destroyed_ship = app.robot.get_ship(cell)

    return Response(is_changed=True, game_status=new_game_status,
                    icon=new_icon, is_ship_destroyed=is_ship_destroyed,
                    destroyed_ship=destroyed_ship).to_dict()


def fire_person_cell(current_status):
    if current_status != GameStatus.BATTLE.value:
        return Response().to_dict()

    fired_cell, fired_cell_status = app.robot.random_fire()
    new_game_status = app.person.check_game_status()
    fired_cell_id = \
        player_cells_to_id_format([fired_cell], PlayerName.PERSON.value)[0]

    if fired_cell_status == CellStatus.DESTROYED.value:
        new_icon = CellIcon.DESTROYED.value
        is_ship_destroyed = app.person.is_ship_destroyed(fired_cell)
    else:
        new_icon = CellIcon.MISFIRE.value
        is_ship_destroyed = False

    destroyed_ship = ''
    if is_ship_destroyed:
        destroyed_ship = app.person.get_ship(fired_cell)

    return Response(is_changed=True, game_status=new_game_status,
                    cells=fired_cell_id, icon=new_icon,
                    is_ship_destroyed=is_ship_destroyed,
                    destroyed_ship=destroyed_ship).to_dict()


def get_opponent_remaining_ship_cells():
    remaining_cells = app.robot.get_remaining_ship_cells()
    cells_ids = player_cells_to_id_format(remaining_cells,
                                          PlayerName.OPPONENT.value)
    return Response(cells=cells_ids, icon=CellIcon.SHIP.value).to_dict()


def cell_id_to_computing_format(cell_id):
    column_row = cell_id.split('_')[-1].split('-')
    column = int(column_numbers_and_letters[column_row[0]]) - 1
    row = int(column_row[1]) - 1
    return row, column


def player_cells_to_id_format(cells, player):
    cells_ids = []
    for cell in cells:
        cells_ids.append(
            f'{player}-board__cell_' +
            f'{column_numbers_and_letters[cell[1] + 1]}-{cell[0] + 1}')

    return cells_ids


@dataclass
class Response:
    is_changed: bool
    game_status: str
    cells: list
    icon: str = CellIcon.EMPTY.value
    is_ship_destroyed: bool = False
    destroyed_ship: str = ''
    ship_count: int = 0
    returned_ship: str = ''

    def __init__(self, is_changed=False,
                 game_status=GameStatus.START.value,
                 cells=None, icon=CellIcon.EMPTY.value,
                 is_ship_destroyed=False, destroyed_ship='', ship_count=0,
                 returned_ship=''):
        self.is_changed = is_changed
        self.game_status = game_status
        self.cells = cells
        self.icon = icon
        self.is_ship_destroyed = is_ship_destroyed
        self.destroyed_ship = destroyed_ship
        self.ship_count = ship_count
        self.returned_ship = returned_ship

    def to_dict(self):
        return {
            'is_changed': self.is_changed,
            'game_status': self.game_status,
            'cells': self.cells,
            'icon': self.icon,
            'is_ship_destroyed': self.is_ship_destroyed,
            'destroyed_ship': self.destroyed_ship,
            'ship_count': self.ship_count,
            'returned_ship': self.returned_ship
        }
