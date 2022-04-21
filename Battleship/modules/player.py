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
cell_misfire = 'Misfire'
cell_destroyed = 'Destroyed'

status_place_ships = 'Ships placing'
status_battle = 'Battle'
status_win = 'Win'
status_lose = 'Lose'


def get_ship_direction(ship_cells):
    if len(ship_cells) == 1 or ship_cells[0][0] == ship_cells[1][0]:
        return direction_horizontal
    return direction_vertical


def get_neighbor_cells(ship_cells):
    ship_direction = get_ship_direction(ship_cells)
    neighbors = []

    if ship_direction == direction_vertical:
        start_row = ship_cells[0][0] - 1
        center_column = ship_cells[0][1]
        neighbors_length = ship_cells[-1][0] - start_row + 2
        for r in range(start_row, start_row + neighbors_length):
            if 0 <= r <= 9:
                neighbors.append([r, center_column])
                if center_column - 1 >= 0:
                    neighbors.append([r, center_column - 1])
                if center_column + 1 <= 9:
                    neighbors.append([r, center_column + 1])

    if ship_direction == direction_horizontal:
        start_column = ship_cells[0][1] - 1
        center_row = ship_cells[0][0]
        neighbors_length = ship_cells[-1][1] - start_column + 2
        for c in range(start_column, start_column + neighbors_length):
            if 0 <= c <= 9:
                neighbors.append([center_row, c])
                if center_row - 1 >= 0:
                    neighbors.append([center_row - 1, c])
                if center_row + 1 <= 9:
                    neighbors.append([center_row + 1, c])

    return neighbors


def get_ship_cells(cell, ship, ship_direction):
    cells = []
    ship_range = ships_ranges[ship]

    if ship_direction == direction_vertical:
        for r in range(ship_range[0], ship_range[1] + 1):
            if 0 <= cell[0] + r <= 9:
                cells.append([cell[0] + r, cell[1]])

    if ship_direction == direction_horizontal:
        for c in range(ship_range[0], ship_range[1] + 1):
            if 0 <= cell[1] + c <= 9:
                cells.append([cell[0], cell[1] + c])

    return cells


class Player:
    def __init__(self):
        self.board = \
            [[cell_empty for column in range(10)] for row in range(10)]
        self.neighbors_board = \
            [[0 for column in range(10)] for row in range(10)]

        self.non_placed_ships_count = 10
        self.ships_remains_to_place = {
            'Battleship': 1,
            'Cruiser': 2,
            'Submarine': 3,
            'Destroyer': 4
        }

        self.ships = {
            'Battleship': [],
            'Cruiser': [],
            'Submarine': [],
            'Destroyer': []
        }

        self.opponent = None

        self.remaining_ship_cells_count = 20
        self.opponent_remaining_ship_cells_count = 20

    def init_opponent(self, opponent):
        self.opponent = opponent

    def fire(self, cell):
        fired_cell_status, is_one_more = self.opponent.get_fired(cell)

        if is_one_more:
            self.opponent_remaining_ship_cells_count -= 1

        return fired_cell_status

    def get_fired(self, cell):
        row, column = cell[0], cell[1]
        current_cell = self.board[row][column]

        fired_cell_status = cell_misfire
        is_one_more = False

        if current_cell == cell_destroyed:
            fired_cell_status = cell_destroyed

        if current_cell in (cell_empty, cell_neighbor):
            self.board[row][column] = cell_misfire

        if current_cell == cell_ship:
            fired_cell_status = cell_destroyed
            self.board[row][column] = cell_destroyed
            self.remaining_ship_cells_count -= 1
            is_one_more = True

        return fired_cell_status, is_one_more

    def place_ship(self, cell, ship, ship_direction):
        if not self.is_placement_correct(cell, ship, ship_direction):
            return []

        ship_cells = get_ship_cells(cell, ship, ship_direction)
        neighbor_cells = get_neighbor_cells(ship_cells)

        for neighbor_cell in neighbor_cells:
            self.board[neighbor_cell[0]][neighbor_cell[1]] = cell_neighbor
        for ship_cell in ship_cells:
            self.board[ship_cell[0]][ship_cell[1]] = cell_ship
        for neighbor_cell in neighbor_cells:
            self.neighbors_board[neighbor_cell[0]][neighbor_cell[1]] += 1

        self.non_placed_ships_count -= 1
        self.ships_remains_to_place[ship] -= 1
        self.ships[ship].append(ship_cells)

        return ship_cells

    def is_placement_correct(self, cell, ship, ship_direction):
        if self.ships_remains_to_place[ship] == 0:
            return False

        row = cell[0]
        column = cell[1]
        ship_range = ships_ranges[ship]

        if ship_direction == direction_vertical:
            if row + ship_range[0] < 0 or row + ship_range[1] > 9:
                return False
            for r in range(ship_range[0], ship_range[1] + 1):
                if self.board[row + r][column] in (cell_neighbor, cell_ship):
                    return False

        if ship_direction == direction_horizontal:
            if column + ship_range[0] < 0 or column + ship_range[1] > 9:
                return False
            for c in range(ship_range[0], ship_range[1] + 1):
                if self.board[row][column + c] in (cell_neighbor, cell_ship):
                    return False

        return True

    def return_ship(self, cell):
        self.non_placed_ships_count += 1

        ship_name = self.get_ship(cell)
        for ship_cells in self.ships[ship_name]:
            for ship_cell in ship_cells:
                if ship_cell == cell:
                    cells = ship_cells
                    self.ships[ship_name].remove(ship_cells)
                    self.ships_remains_to_place[ship_name] += 1
                    self._uninit_ship(ship_name, cells)
                    return cells
        return None

    def _uninit_ship(self, ship, cells):
        ship_range = ships_ranges[ship]
        ship_direction = get_ship_direction(cells)
        reset_length = abs(ship_range[0]) + ship_range[1] + 3

        if ship_direction == direction_vertical:
            start_r = cells[0][0] - 1
            center_c = cells[0][1]
            for r in range(start_r, start_r + reset_length):
                if 0 <= r <= 9:
                    self.neighbors_board[r][center_c] -= 1
                    self.board[r][center_c] = cell_empty
                    if center_c - 1 >= 0:
                        self._uninit_cell(r, center_c - 1)
                    if center_c + 1 <= 9:
                        self._uninit_cell(r, center_c + 1)

        if ship_direction == direction_horizontal:
            start_c = cells[0][1] - 1
            center_r = cells[0][0]
            for c in range(start_c, start_c + reset_length):
                if 0 <= c <= 9:
                    self.neighbors_board[center_r][c] -= 1
                    self.board[center_r][c] = cell_empty
                    if center_r - 1 >= 0:
                        self._uninit_cell(center_r - 1, c)
                    if center_r + 1 <= 9:
                        self._uninit_cell(center_r + 1, c)

    def _uninit_cell(self, row, column):
        self.neighbors_board[row][column] -= 1
        if self.board[row][column] == cell_ship or \
                self.neighbors_board[row][column] == 0:
            self.board[row][column] = cell_empty

    def check_game_status(self):
        if self.non_placed_ships_count > 0:
            return status_place_ships

        if self.opponent_remaining_ship_cells_count == 0:
            return status_win

        if self.remaining_ship_cells_count == 0:
            return status_lose

        return status_battle

    def get_ship_count(self, ship):
        return self.ships_remains_to_place[ship]

    def get_ship(self, cell):
        for ships_item in self.ships.items():
            for ship in ships_item[1]:
                for ship_cell in ship:
                    if ship_cell == cell:
                        return ships_item[0]
        return None
