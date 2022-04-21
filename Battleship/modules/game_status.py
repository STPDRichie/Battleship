import app
from modules.player import get_ship_cells, ships_ranges

status_start = 'Start game'
status_place_ships = 'Ships placing'
status_battle = 'Battle'
status_win = 'Win'
status_lose = 'Lose'

icon_empty = '<i class="fa-solid"></i>'
icon_ship = '<i class="fa-solid fa-circle"></i>'
icon_destroyed = '<i class="fa-solid fa-circle-xmark"></i>'
icon_misfire = '<i class="fa-regular fa-circle"></i>'

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
    if current_status != status_start:
        return {'is_changed': False}

    game_status = status_place_ships
    game_status_remove_class = 'game_status'
    game_status_add_class = 'game_status-inactive'

    app.person.__init__()
    app.robot.__init__()

    app.person.init_opponent(app.robot)
    app.robot.init_opponent(app.person)
    app.robot.init_board()

    return {
        'is_changed': True,
        'game_status': game_status,
        'game_status_remove_class': game_status_remove_class,
        'game_status_add_class': game_status_add_class
    }


def get_person_outline_cells(ship, ship_direction,
                             cell_id, current_status):
    if current_status != status_place_ships:
        return {'is_changed': False}

    cell = cell_id_to_computing_format(cell_id)
    cells = get_ship_cells(cell, ship, ship_direction)

    ship_length = abs(ships_ranges[ship][0]) + ships_ranges[ship][1] + 1
    if len(cells) != ship_length:
        return {'is_changed': False}

    cells_ids = player_cells_to_id_format(cells, 'person')

    return {
        'is_changed': True,
        'cells': cells_ids
    }


def change_person_cells(cell_icon, cell_id, ship,
                        ship_direction, current_status):
    if current_status != status_place_ships:
        return {'is_changed': False}

    cell = cell_id_to_computing_format(cell_id)

    if cell_icon == icon_empty:
        returned_ship = ''
        ship_cells = app.person.place_ship(cell, ship, ship_direction)
        if not ship_cells:
            return {'is_changed': False}
        new_game_status = app.person.check_game_status()
        cells_ids = player_cells_to_id_format(ship_cells, 'person')
        ship_count = app.person.get_ship_count(ship)
        new_icon = icon_ship
    elif cell_icon == icon_ship:
        returned_ship = app.person.get_ship(cell)
        ship_cells = app.person.return_ship(cell)
        new_game_status = app.person.check_game_status()
        cells_ids = player_cells_to_id_format(ship_cells, 'person')
        ship_count = app.person.get_ship_count(returned_ship)
        new_icon = icon_empty
    else:
        return {'is_changed': False}

    return {
        'is_changed': True,
        'game_status': new_game_status,
        'ship_count': ship_count,
        'returned_ship': returned_ship,
        'cells': cells_ids,
        'cells_icon': new_icon
    }


def fire_opponent_cell(cell_id, current_status):
    if current_status != status_battle:
        return {'is_changed': False}

    cell = cell_id_to_computing_format(cell_id)
    fired_cell_status = app.person.fire(cell)
    new_game_status = app.person.check_game_status()

    if fired_cell_status == 'Destroyed':
        new_icon = icon_destroyed
    else:
        new_icon = icon_misfire

    return {
        'is_changed': True,
        'game_status': new_game_status,
        'cell_icon': new_icon
    }


def fire_person_cell(current_status):
    if current_status != status_battle:
        return {'is_changed': False}

    fired_cell, fired_cell_status = app.robot.random_fire()
    new_game_status = app.person.check_game_status()
    fired_cell_id = player_cells_to_id_format([fired_cell], 'person')[0]

    if fired_cell_status == 'Destroyed':
        new_icon = icon_destroyed
    else:
        new_icon = icon_misfire

    return {
        'is_changed': True,
        'game_status': new_game_status,
        'cell': fired_cell_id,
        'cell_icon': new_icon
    }


def get_opponent_remaining_ship_cells():
    remaining_cells = app.robot.get_remaining_ship_cells()
    cells_ids = player_cells_to_id_format(remaining_cells, 'opponent')
    return {
        'cells': cells_ids,
        'cell_icon': icon_ship
    }


def cell_id_to_computing_format(cell_id):
    id_split = cell_id.split('-')
    column = int(column_numbers_and_letters[id_split[-2]]) - 1
    row = int(id_split[-1]) - 1
    return [row, column]


def player_cells_to_id_format(cells, player):
    cells_ids = []
    for cell in cells:
        cells_ids.append(
            f'{player}-board_cell-' +
            f'{column_numbers_and_letters[cell[1] + 1]}-{cell[0] + 1}')

    return cells_ids
