import app

status_text_start = 'Start game'
status_text_place_ships = 'Ships placing'
status_text_battle = 'Battle'

icon_empty = '<i class="fa-solid"></i>'
icon_ship = '<i class="fa-solid fa-circle"></i>'
icon_destroyed = '<i class="fa-solid fa-circle-xmark"></i>'
icon_missfire = '<i class="fa-regular fa-circle"></i>'

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

ships_ranges = {
    'Battleship': [-1, 2],
    'Cruiser': [-1, 1],
    'Submarine': [0, 1],
    'Destroyer': [0, 0]
}


def change_game_status(current_status):
    if current_status == status_text_start:
        game_status = status_text_place_ships
        game_status_remove_class = 'game_status'
        game_status_add_class = 'game_status-inactive'
        app.person.__init__()
        app.opponent.__init__()
        return {'is_changed': True,
                'game_status': game_status,
                'game_status_remove_class': game_status_remove_class,
                'game_status_add_class': game_status_add_class}
    return {'is_changed': False}


def change_player_cell(cell_icon, cell_id_text,
                       current_ship, ship_direction,
                       current_status):
    if current_status == status_text_start or \
            current_status != status_text_place_ships:
        return {'is_changed': False}

    cell_id = [int(column_numbers_and_letters[cell_id_text.split('-')[-2]]),
               int(cell_id_text.split('-')[-1])]

    if cell_icon == icon_empty and app.person\
            .is_placement_correct(cell_id, current_ship, ship_direction):
        cell_ids = app.person.place_ship(cell_id, current_ship, ship_direction)
        cells = cells_to_id_format(cell_ids)
        new_status = app.person.get_game_status()
        ship_count = app.person.get_ship_count(current_ship)
        return {'is_changed': True,
                'game_status': new_status,
                'ship_count': ship_count,
                'returned_ship': '',
                'cells': cells,
                'cells_icon': icon_ship}

    if cell_icon == icon_ship:
        returned_ship = app.person.get_ship(cell_id)
        cell_ids = app.person.remove_ship(cell_id)
        ship_count = app.person.get_ship_count(returned_ship)
        cells = cells_to_id_format(cell_ids)
        return {'is_changed': True,
                'game_status': status_text_place_ships,
                'ship_count': ship_count,
                'returned_ship': returned_ship,
                'cells': cells,
                'cells_icon': icon_empty}

    return {'is_changed': False}


def change_opponent_cell(cell_icon, cell_id_text, current_status):
    if current_status != status_text_battle:
        return {'is_changed': False}

    cell_id = [int(column_numbers_and_letters[cell_id_text.split('-')[-2]]),
               int(cell_id_text.split('-')[-1])]
    if cell_icon == icon_ship:
        return {'is_changed': True,
                'game_status': status_text_battle,
                'cell_icon': icon_destroyed}
    elif cell_icon == icon_empty:
        return {'is_changed': True,
                'game_status': status_text_battle,
                'cell_icon': icon_missfire}

    return {'is_changed': False}


def cells_to_id_format(cell_ids):
    cells = []
    for cell_id in cell_ids:
        cells.append(
            'person-board_cell-' +
            '{0}-{1}'.format(
                column_numbers_and_letters[cell_id[0]],
                cell_id[1])
        )
    return cells
