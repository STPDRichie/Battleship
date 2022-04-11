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

status_place_ships = 'Ships placing'
status_battle = 'Battle'
status_win = 'Win'
status_lose = 'Lose'


def get_ship_direction(cells):
    if len(cells) == 1 or cells[0][1] == cells[1][1]:
        return direction_horizontal
    return direction_vertical


def get_neighbor_cells(ship_cells):
    ship_direction = get_ship_direction(ship_cells)
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


def get_ship_cells(cell_id, ship, ship_direction):
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
        self.board = \
            [[cell_empty for row in range(10)] for column in range(10)]
        self.neighbors_board = \
            [[0 for row in range(10)] for column in range(10)]
        self.remaining_ship_cells_count = 20
        self.opponent_remaining_ship_cells_count = 20

        self.non_placed_ships_count = 10

        self.ships = {
            'Battleship': [],
            'Cruiser': [],
            'Submarine': [],
            'Destroyer': []
        }

        self.ships_neighbor_cells = {
            'Battleship': [],
            'Cruiser': [],
            'Submarine': [],
            'Destroyer': []
        }

    def fire(self, cell_id):
        fire_result = app.opponent.get_fired(cell_id)
        game_status = status_battle
        cell_status = cell_missfire
        if fire_result == cell_destroyed:
            self.opponent_remaining_ship_cells_count -= 1
            print('op_ships', self.opponent_remaining_ship_cells_count)  # todo
            cell_status = cell_destroyed
        if self.opponent_remaining_ship_cells_count == 0:
            game_status = status_win
        return game_status, cell_status

    def get_fired(self, cell_id):
        if self.board[cell_id[1] - 1][cell_id[0] - 1] == cell_empty or \
                self.board[cell_id[1] - 1][cell_id[0] - 1] == cell_neighbor:
            self.board[cell_id[1] - 1][cell_id[0] - 1] = cell_missfire
            return cell_missfire
        if self.board[cell_id[1] - 1][cell_id[0] - 1] == cell_ship:
            self.board[cell_id[1] - 1][cell_id[0] - 1] = cell_destroyed
            self.remaining_ship_cells_count -= 1
            return cell_destroyed

    def place_ship(self, cell_id, ship, ship_direction):
        ship_cells = get_ship_cells(cell_id, ship, ship_direction)
        neighbor_cells = get_neighbor_cells(ship_cells)
        self.ships_neighbor_cells[ship].append(neighbor_cells)

        for cell in neighbor_cells:
            self.board[cell[1] - 1][cell[0] - 1] = cell_neighbor
        for cell in ship_cells:
            self.board[cell[1] - 1][cell[0] - 1] = cell_ship

        self.non_placed_ships_count -= 1
        self._init_ship(ship, ship_cells)
        return ship_cells

    def _init_ship(self, ship, ship_cells):
        self._ships_remains_to_place[ship] -= 1
        ship_neighbor_cells = get_neighbor_cells(ship_cells)
        for cell in ship_neighbor_cells:
            self.neighbors_board[cell[1] - 1][cell[0] - 1] += 1
        self.ships[ship].append(ship_cells)

    def is_placement_correct(self, cell_id, ship, ship_direction):
        if self._ships_remains_to_place[ship] == 0:
            return False

        if ship_direction == direction_vertical:
            if cell_id[1] + ships_ranges[ship][0] < 1 or \
                    cell_id[1] + ships_ranges[ship][1] > 10:
                return False
            for r in range(ships_ranges[ship][0], ships_ranges[ship][1] + 1):
                if self.board[cell_id[1] + r - 1][cell_id[0] - 1] \
                        == cell_neighbor:
                    return False

        elif ship_direction == direction_horizontal:
            if cell_id[0] + ships_ranges[ship][0] < 1 or \
                    cell_id[0] + ships_ranges[ship][1] > 10:
                return False
            for c in range(ships_ranges[ship][0], ships_ranges[ship][1] + 1):
                if self.board[cell_id[1] - 1][cell_id[0] + c - 1] \
                        == cell_neighbor:
                    return False

        return True

    def remove_ship(self, cell_id):
        self.non_placed_ships_count += 1
        current_ship = self.get_ship(cell_id)
        for ship in self.ships[current_ship]:
            for cell in ship:
                if cell == cell_id:
                    cells = ship
                    self.ships[current_ship].remove(ship)
                    self._ships_remains_to_place[current_ship] += 1
                    self._uninit_ship(current_ship, cells)
                    return cells

    def _uninit_ship(self, ship, cells):
        ship_range = ships_ranges[ship]
        ship_direction = get_ship_direction(cells)
        reset_length = abs(ship_range[0]) + ship_range[1] + 3
        if ship_direction == direction_vertical:
            start_r = cells[0][1] - 2
            center_c = cells[0][0] - 1
            for r in range(start_r, start_r + reset_length):
                if 0 <= r <= 9:
                    self.neighbors_board[r][center_c] -= 1
                    self.board[r][center_c] = cell_empty
                    if center_c - 1 > 0:
                        self.neighbors_board[r][center_c - 1] -= 1
                        if self.board[r][center_c - 1] == cell_ship or \
                                self.neighbors_board[r][center_c - 1] == 0:
                            self.board[r][center_c - 1] = cell_empty
                    if center_c + 1 < 10:
                        self.neighbors_board[r][center_c + 1] -= 1
                        if self.board[r][center_c + 1] == cell_ship or \
                                self.neighbors_board[r][center_c + 1] == 0:
                            self.board[r][center_c + 1] = cell_empty

        elif ship_direction == direction_horizontal:
            start_c = cells[0][0] - 2
            center_r = cells[0][1] - 1
            for c in range(start_c, start_c + reset_length):
                if 0 <= c <= 9:
                    self.neighbors_board[center_r][c] -= 1
                    self.board[center_r][c] = cell_empty
                    if center_r - 1 > 0:
                        self.neighbors_board[center_r - 1][c] -= 1
                        if self.board[center_r - 1][c] == cell_ship or \
                                self.neighbors_board[center_r - 1][c] == 0:
                            self.board[center_r - 1][c] = cell_empty
                    if center_r + 1 < 10:
                        self.neighbors_board[center_r + 1][c] -= 1
                        if self.board[center_r + 1][c] == cell_ship or \
                                self.neighbors_board[center_r + 1][c] == 0:
                            self.board[center_r + 1][c] = cell_empty

    def check_game_status(self):
        if self.non_placed_ships_count == 0:
            return status_battle
        return status_place_ships

    def get_ship_count(self, ship):
        return self._ships_remains_to_place[ship]

    def get_ship(self, cell_id):
        for ship_name in self.ships.keys():
            for ship in self.ships[ship_name]:
                for cell in ship:
                    if cell == cell_id:
                        return ship_name
