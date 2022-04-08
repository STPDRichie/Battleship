status_text_start = 'Start game'
status_text_place_ships = 'Ships placing'
status_text_battle = 'Battle'

needs_text_start = 'Click the button to start game'
needs_text_place = 'Place ship'

icon_solid = '<i class="fa-solid"></i>'
icon_circle = '<i class="fa-solid fa-circle"></i>'
icon_crossedCircle = '<i class="fa-solid fa-circle-xmark"></i>'
icon_emptyCircle = '<i class="fa-regular fa-circle"></i>'


def change_game_status(current_status, current_needs):
    if current_status == status_text_start:
        game_status = status_text_place_ships
        game_needs = needs_text_place
        game_status_remove_class = 'game_status'
        game_status_add_class = 'game_status-inactive'
    elif current_status == status_text_place_ships:
        game_status = status_text_start
        game_needs = needs_text_start
        game_status_remove_class = 'game_status-inactive'
        game_status_add_class = 'game_status'
    elif current_status == status_text_battle:
        game_status = status_text_start
        game_needs = needs_text_start
        game_status_remove_class = 'game_status-inactive'
        game_status_add_class = 'game_status'

    return {'game_status': game_status,
            'game_needs': game_needs,
            'game_status_remove_class': game_status_remove_class,
            'game_status_add_class': game_status_add_class}


def change_board_cell(board, current_status, cell):
    if board == 'player':
        if current_status != status_text_start:
            return {'is_changed': True,
                    'game_status': status_text_battle,
                    'cell': icon_emptyCircle}

    return {'is_changed': False}
