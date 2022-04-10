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

direction_vertical = 'Vertical'
direction_horizontal = 'Horizontal'

status_text_place_ships = 'Ships placing'
status_text_battle = 'Battle'


class Player:
    def __init__(self):
        self._ships_remains_to_place = {
            'Battleship': 1,
            'Cruiser': 2,
            'Submarine': 3,
            'Destroyer': 4
        }
        self._board = [['Empty' for column in range(10)] for row in range(10)]

        self._ship_count = 10
        self._battleship = None
        self._cruisers = []
        self._submarines = []
        self._destroyers = []

    def fire(self, cell_id):
        pass

    def place_ship(self, cell_id, ship, ship_direction):
        cells = []
        ship_range = ships_ranges[ship]
        if ship_direction == direction_vertical:
            for r in range(ship_range[0] - 1, ship_range[1] + 2):
                if 0 < cell_id[1] + r < 10:
                    self._board[cell_id[0] - 1][cell_id[1] - 1 + r] \
                        = 'Neighbour'
                    if cell_id[0] - 2 >= 0:
                        self._board[cell_id[0] - 2][cell_id[1] - 1 + r] \
                            = 'Neighbour'
                    if cell_id[0] <= 9:
                        self._board[cell_id[0]][cell_id[1] - 1 + r] \
                            = 'Neighbour'
            for r in range(ship_range[0], ship_range[1] + 1):
                self._board[cell_id[0] - 1][cell_id[1] - 1 + r] = 'Ship'
                cells.append([cell_id[0], cell_id[1] + r])

        elif ship_direction == direction_horizontal:
            for c in range(ship_range[0] - 1, ship_range[1] + 2):
                if 0 < cell_id[0] + c < 10:
                    self._board[cell_id[0] - 1 + c][cell_id[1] - 1] \
                        = 'Neighbour'
                    if cell_id[1] - 2 >= 0:
                        self._board[cell_id[0] - 1 + c][cell_id[1] - 2] \
                            = 'Neighbour'
                    if cell_id[1] <= 9:
                        self._board[cell_id[0] - 1 + c][cell_id[1]] \
                            = 'Neighbour'
            for c in range(ship_range[0], ship_range[1] + 1):
                self._board[cell_id[0] - 1 + c][cell_id[1] - 1] = 'Ship'
                cells.append([cell_id[0] + c, cell_id[1]])

        self._ship_count -= 1
        self._init_ship(ship, cells)
        return cells

    def _init_ship(self, ship, ship_cells):
        self._ships_remains_to_place[ship] -= 1
        if ship == 'Battleship':
            self._battleship = ship_cells
        if ship == 'Cruiser':
            self._cruisers.append(ship_cells)
        if ship == 'Submarine':
            self._submarines.append(ship_cells)
        if ship == 'Destroyer':
            self._destroyers.append(ship_cells)

    def is_placement_correct(self, cell_id, ship, ship_direction):
        if ship_direction == direction_vertical:
            if cell_id[1] + ships_ranges[ship][0] < 1 or \
                    cell_id[1] + ships_ranges[ship][1] > 10:
                return False
            for r in range(ships_ranges[ship][0], ships_ranges[ship][1] + 1):
                if self._board[cell_id[0] - 1][cell_id[1] + r - 1] \
                        == 'Neighbour':
                    return False

        elif ship_direction == direction_horizontal:
            if cell_id[0] + ships_ranges[ship][0] < 1 or \
                    cell_id[0] + ships_ranges[ship][1] > 10:
                return False
            for c in range(ships_ranges[ship][0], ships_ranges[ship][1] + 1):
                if self._board[cell_id[0] + c - 1][cell_id[1] - 1] \
                        == 'Neighbour':
                    return False

        return True

    def remove_ship(self, cell_id):
        self._ship_count += 1

    def check_game_status(self):
        if self._ship_count == 0:
            return status_text_battle
        return status_text_place_ships

    def check_ship_count(self, ship):
        return self._ships_remains_to_place[ship]
