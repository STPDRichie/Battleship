status_text_start = 'Start game'
status_text_place_ships = 'Ships placing'
status_text_battle = 'Battle'

needs_text_start = 'Click the button to start game'
needs_text_place_battleship = 'Place battleship'
needs_text_place_cruiser = 'Place cruiser'
needs_text_place_submarine = 'Place submarine'
needs_text_place_destroyer = 'Place destroyer'
needs_text_battle = 'Let\'s begin the war'

icon_solid = '<i class="fa-solid"></i>'
icon_circle = '<i class="fa-solid fa-circle"></i>'
icon_crossedCircle = '<i class="fa-solid fa-circle-xmark"></i>'
icon_emptyCircle = '<i class="fa-regular fa-circle"></i>'

board_column_numbers = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'f': 6,
    'g': 7,
    'h': 8,
    'i': 9,
    'j': 10
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


def change_board_cell(board,
                      current_status, current_needs,
                      cell_icon, cell_id):
    current_ship = current_needs.split()[1]
    if current_status == status_text_start:
        return {'is_changed': False}

    if current_status == status_text_place_ships:
        if board == 'player':
            return change_player_cell(cell_icon, cell_id)
        return {'is_changed': False}

    if current_status == status_text_battle:
        if board == 'ai':
            return change_ai_cell(cell_icon)
        return {'is_changed': False}

    return {'is_changed': False}


def change_player_cell(cell_icon, cell_id):
    if cell_icon == icon_solid and is_placement_cell_correct(cell_id):
        return {'is_changed': True,
                'game_status': status_text_place_ships,
                'cell': icon_circle}
    elif cell_icon == icon_circle:
        return {'is_changed': True,
                'game_status': status_text_place_ships,
                'cell': icon_solid}

    return {'is_changed': False}


def is_placement_cell_correct(cell_id_text):
    cell_id_text_splitted = cell_id_text.split('-')
    cell_id = [int(board_column_numbers[cell_id_text_splitted[-2]]),
               int(cell_id_text_splitted[-1])]
    print(cell_id)
    if cell_id[1] > 8 or cell_id[1] < 2:
        return False
    return True


def change_ai_cell(cell):
    if cell == icon_circle:
        return {'is_changed': True,
                'game_status': status_text_battle,
                'cell': icon_crossedCircle}
    elif cell == icon_solid:
        return {'is_changed': True,
                'game_status': status_text_battle,
                'cell': icon_emptyCircle}

    return {'is_changed': False}
