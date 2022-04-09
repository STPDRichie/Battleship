status_text_start = 'Start game'
status_text_place_ships = 'Ships placing'
status_text_battle = 'Battle'

needs_text_start = 'Click the button to start game'
needs_text_place_battleship = 'Place battleship'
needs_text_place_cruiser = 'Place cruiser'
needs_text_place_submarine = 'Place submarine'
needs_text_place_destroyer = 'Place destroyer'
needs_text_battle = 'Let\'s begin the war'

ship_direction_vertical = 'Vertical'
ship_direction_horizontal = 'Horizontal'

icon_solid = '<i class="fa-solid"></i>'
icon_circle = '<i class="fa-solid fa-circle"></i>'
icon_crossedCircle = '<i class="fa-solid fa-circle-xmark"></i>'
icon_emptyCircle = '<i class="fa-regular fa-circle"></i>'

board_column_numbers = {
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

ships_range = {
    'battleship': range(-1, 3),
    'cruiser': range(-1, 2),
    'submarine': range(2),
    'destroyer': range(1)
}


def change_game_status(current_status):
    if current_status == status_text_start:
        game_status = status_text_place_ships
        game_needs = needs_text_place_battleship
        game_status_remove_class = 'game_status'
        game_status_add_class = 'game_status-inactive'
    elif current_status == status_text_place_ships:
        game_status = status_text_battle
        game_needs = needs_text_battle
        game_status_remove_class = 'game_status-inactive'
        game_status_add_class = 'game_status-inactive'
    elif current_status == status_text_battle:
        game_status = status_text_start
        game_needs = needs_text_start
        game_status_remove_class = 'game_status-inactive'
        game_status_add_class = 'game_status'

    return {'game_status': game_status,
            'game_needs': game_needs,
            'game_status_remove_class': game_status_remove_class,
            'game_status_add_class': game_status_add_class}


# def change_board_cell(board,
#                       ship_direction,
#                       current_status, current_needs,
#                       cell_icon, cell_id_text):
#     current_ship = current_needs.split()[1]
#
#     if current_status == status_text_place_ships:
#         if board == 'player':
#             return change_player_cell(
#                 cell_icon,
#                 cell_id_text,
#                 current_ship,
#                 ship_direction)
#         return {'is_changed': False}
#
#     if current_status == status_text_battle:
#         if board == 'ai':
#             return change_ai_cell(cell_icon)
#         return {'is_changed': False}
#
#     return {'is_changed': False}


def change_player_cell(cell_icon, cell_id_text,
                       current_ship, ship_direction,
                       current_status):
    if current_status == status_text_start or \
            current_status != status_text_place_ships:
        return {'is_changed': False}

    cell_id = [int(board_column_numbers[cell_id_text.split('-')[-2]]),
               int(cell_id_text.split('-')[-1])]
    if cell_icon == icon_solid and \
            is_placement_cell_correct(cell_id, ship_direction):
        cells = cells_to_id_format(
            get_neighbour_cells(cell_id, current_ship, ship_direction)
        )
        return {'is_changed': True,
                'game_status': status_text_place_ships,
                'cells': cells,
                'cells_icon': icon_circle}

    if cell_icon == icon_circle:
        return {'is_changed': True,
                'game_status': status_text_place_ships,
                'cells': cells_to_id_format([cell_id]),
                'cells_icon': icon_solid}

    return {'is_changed': False}


def change_ai_cell(cell_icon, cell_id_text, current_status):
    if current_status != status_text_battle:
        return {'is_changed': False}

    cell_id = [int(board_column_numbers[cell_id_text.split('-')[-2]]),
               int(cell_id_text.split('-')[-1])]
    if cell_icon == icon_circle:
        return {'is_changed': True,
                'game_status': status_text_battle,
                'cell_icon': icon_crossedCircle}
    elif cell_icon == icon_solid:
        return {'is_changed': True,
                'game_status': status_text_battle,
                'cell_icon': icon_emptyCircle}

    return {'is_changed': False}


def is_placement_cell_correct(cell_id, direction):
    if direction == ship_direction_vertical:
        if cell_id[1] > 8 or cell_id[1] < 2:
            return False
    elif direction == ship_direction_horizontal:
        if cell_id[0] > 8 or cell_id[0] < 2:
            return False
    return True


def get_neighbour_cells(cell_id, ship, ship_direction):
    print(cell_id)
    cells = []
    if ship_direction == ship_direction_vertical:
        for i in ships_range[ship]:
            cells.append([cell_id[0], cell_id[1] + i])
    elif ship_direction == ship_direction_horizontal:
        for i in ships_range[ship]:
            cells.append([cell_id[0] + i, cell_id[1]])
    return cells


def cells_to_id_format(cell_ids):
    cells = []
    for cell_id in cell_ids:
        cells.append(
            'player-board_cell-' +
            '{0}-{1}'.format(board_column_numbers[cell_id[0]], cell_id[1])
        )
    return cells
