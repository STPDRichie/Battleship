import app

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

cell_empty = 'Empty'
cell_ship = 'Ship'
cell_neighbor = 'Neighbor'
cell_missfire = 'Missfire'
cell_destroyed = 'Destroyed'

status_text_place_ships = 'Ships placing'
status_text_battle = 'Battle'


def _get_ship_direction(cells):
    if len(cells) == 1 or cells[0][1] == cells[1][1]:
        return direction_horizontal
    return direction_vertical


def _get_neighbor_cells(ship_cells):
    ship_direction = _get_ship_direction(ship_cells)
    neighbors = []
    if ship_direction == direction_vertical:
        start_row = ship_cells[0][1] - 1
        center_column = ship_cells[0][0]
        neighbors_length = ship_cells[-1][1] - start_row + 2
        for r in range(start_row, start_row + neighbors_length):
            if 1 <= r <= 10:
                neighbors.append([center_column, r])
                if center_column - 1 >= 1:
                    neighbors.append([center_column - 1, r])
                if center_column + 1 <= 10:
                    neighbors.append([center_column + 1, r])

    elif ship_direction == direction_horizontal:
        start_column = ship_cells[0][0] - 1
        center_row = ship_cells[0][1]
        neighbors_length = ship_cells[-1][0] - start_column + 2
        for c in range(start_column, start_column + neighbors_length):
            if 1 <= c <= 10:
                neighbors.append([c, center_row])
                if center_row - 1 >= 1:
                    neighbors.append([c, center_row - 1])
                if center_row + 1 <= 10:
                    neighbors.append([c, center_row + 1])

    return neighbors


def _get_ship_cells(cell_id, ship, ship_direction):
    cells = []
    if ship_direction == direction_vertical:
        for r in range(ships_ranges[ship][0], ships_ranges[ship][1] + 1):
            cells.append([cell_id[0], cell_id[1] + r])
    if ship_direction == direction_horizontal:
        for c in range(ships_ranges[ship][0], ships_ranges[ship][1] + 1):
            cells.append([cell_id[0] + c, cell_id[1]])
    return cells


class Player:
    def __init__(self):
        self._ships_remains_to_place = {
            'Battleship': 1,
            'Cruiser': 2,
            'Submarine': 3,
            'Destroyer': 4
        }
        self._board = [['Empty' for column in range(10)] for row in range(10)]
        self._remaining_ship_cells_count = 20
        self._opponent_remaining_ship_cells_count = 20

        self._non_placed_ships_count = 10

        self._battleship = []
        self._cruisers = []
        self._submarines = []
        self._destroyers = []

        # self.ships = {
        #     'Battleship': [],
        #     'Cruiser': [],
        #     'Submarine': [],
        #     'Destroyer': []
        # }

        self._ships_neighbor_cells = {
            'Battleship': [],
            'Cruiser': [],
            'Submarine': [],
            'Destroyer': []
        }

    def fire(self, cell_id):
        fire_result = app.opponent.get_fired(cell_id)
        if fire_result == 'Destroyed':
            self._opponent_remaining_ship_cells_count -= 1
        if self._opponent_remaining_ship_cells_count == 0:
            return 'Win'
        return 'Battle'

    def get_fired(self, cell_id):
        if self._board[cell_id[0] - 1][cell_id[1] - 1] == cell_empty or \
                self._board[cell_id[0] - 1][cell_id[1] - 1] == cell_neighbor:
            self._board[cell_id[0] - 1][cell_id[1] - 1] = cell_missfire
            return cell_missfire
        if self._board[cell_id[0] - 1][cell_id[1] - 1] == cell_ship:
            self._board[cell_id[0] - 1][cell_id[1] - 1] = cell_destroyed
            self._remaining_ship_cells_count -= 1
        if self._remaining_ship_cells_count == 0:
            return 'Lose'
        return cell_destroyed

    def place_ship(self, cell_id, ship, ship_direction):
        ship_cells = _get_ship_cells(cell_id, ship, ship_direction)
        neighbor_cells = _get_neighbor_cells(ship_cells)
        self._ships_neighbor_cells[ship].append(neighbor_cells)

        for cell in neighbor_cells:
            self._board[cell[0] - 1][cell[1] - 1] = cell_neighbor
        for cell in ship_cells:
            self._board[cell[0] - 1][cell[1] - 1] = cell_ship

        self._non_placed_ships_count -= 1
        self._init_ship(ship, ship_cells)
        return ship_cells

    def _init_ship(self, ship, ship_cells):
        self._ships_remains_to_place[ship] -= 1
        if ship == 'Battleship':
            self._battleship.append(ship_cells)
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
                        == cell_neighbor:
                    return False

        elif ship_direction == direction_horizontal:
            if cell_id[0] + ships_ranges[ship][0] < 1 or \
                    cell_id[0] + ships_ranges[ship][1] > 10:
                return False
            for c in range(ships_ranges[ship][0], ships_ranges[ship][1] + 1):
                if self._board[cell_id[0] + c - 1][cell_id[1] - 1] \
                        == cell_neighbor:
                    return False

        return True

    def remove_ship(self, cell_id):
        self._non_placed_ships_count += 1
        ship = self.get_ship(cell_id)
        if ship == 'Battleship':
            for battleship in self._battleship:
                for cell in battleship:
                    if cell == cell_id:
                        cells = battleship
                        self._battleship.remove(battleship)
                        self._ships_remains_to_place[ship] += 1
                        self._reset_cells(cells, ship)
                        return cells
        if ship == 'Cruiser':
            for cruiser in self._cruisers:
                for cell in cruiser:
                    if cell == cell_id:
                        cells = cruiser
                        self._cruisers.remove(cruiser)
                        self._ships_remains_to_place[ship] += 1
                        self._reset_cells(cells, ship)
                        return cells
        if ship == 'Submarine':
            for submarine in self._submarines:
                for cell in submarine:
                    if cell == cell_id:
                        cells = submarine
                        self._submarines.remove(submarine)
                        self._ships_remains_to_place[ship] += 1
                        self._reset_cells(cells, ship)
                        return cells
        if ship == 'Destroyer':
            for destroyer in self._destroyers:
                for cell in destroyer:
                    if cell == cell_id:
                        cells = destroyer
                        self._destroyers.remove(destroyer)
                        self._ships_remains_to_place[ship] += 1
                        self._reset_cells(cells, ship)
                        return cells

    def _uninit_ship(self, ship, ship_cells):
        pass

    def _reset_cells(self, cells, ship):
        ship_range = ships_ranges[ship]
        ship_direction = _get_ship_direction(cells)
        reset_length = abs(ship_range[0]) + ship_range[1] + 3
        if ship_direction == direction_vertical:
            start_row = cells[0][1] - 2
            center_column = cells[0][0] - 1
            for r in range(start_row, start_row + reset_length):
                if 0 <= r <= 9:
                    self._board[center_column][r] = cell_empty
                    if center_column - 1 > 0:
                        self._board[center_column - 1][r] = cell_empty
                    if center_column + 1 < 10:
                        self._board[center_column + 1][r] = cell_empty

        elif ship_direction == direction_horizontal:
            start_column = cells[0][0] - 2
            center_row = cells[0][1] - 1
            for c in range(start_column, start_column + reset_length):
                if 0 <= c <= 9:
                    self._board[c][center_row] = cell_empty
                    if center_row - 1 > 0:
                        self._board[c][center_row - 1] = cell_empty
                    if center_row + 1 < 10:
                        self._board[c][center_row + 1] = cell_empty

    def _get_ship_count_at_neighbor_cell(self, cell_id):
        pass

    def _cell_is_not_anyone_neighbor(self, cell_id, ship):
        pass

    def check_game_status(self):
        if self._non_placed_ships_count == 0:
            return status_text_battle
        return status_text_place_ships

    def get_ship_count(self, ship):
        return self._ships_remains_to_place[ship]

    def get_ship(self, cell_id):
        for battleship in self._battleship:
            for cell in battleship:
                if cell == cell_id:
                    return 'Battleship'
        for cruiser in self._cruisers:
            for cell in cruiser:
                if cell == cell_id:
                    return 'Cruiser'
        for submarine in self._submarines:
            for cell in submarine:
                if cell == cell_id:
                    return 'Submarine'
        for destroyer in self._destroyers:
            for cell in destroyer:
                if cell == cell_id:
                    return 'Destroyer'
