from modules.domain import GameStatus, CellStatus, ShipDirection, BoardData
from modules.ship import Ship


def get_ship_direction(ship_cells):
    if len(ship_cells) == 1 or ship_cells[0][0] == ship_cells[1][0]:
        return ShipDirection.HORIZONTAL.value
    return ShipDirection.VERTICAL.value


class Player:
    def __init__(self, board_data: BoardData):
        self.board_size = board_data.get_board_size()
        self.min_cell = board_data.get_min_cell_index()
        self.max_cell = board_data.get_max_cell_index()
        
        self.board = \
            [[CellStatus.EMPTY.value for _ in range(self.board_size)]
             for _ in range(self.board_size)]
        self.neighbors_board = [[0 for _ in range(self.board_size)]
                                for _ in range(self.board_size)]
        
        self.non_placed_ships_count = board_data.get_non_placed_ships_count()
        self.ships_remains_to_place = board_data.get_ships_remains_to_place()
        self.ships_ranges = board_data.get_ships_ranges()
        
        self.ships = []
        
        self.opponent = None
        
        self.remaining_ship_cells_count = board_data.get_ship_cells_count()
        self.destroyed_ship_cells = []
    
    def init_opponent(self, opponent):
        self.opponent = opponent
    
    def fire(self, cell):
        fired_cell_status = self.opponent.get_fired(cell)
        return fired_cell_status
    
    def get_fired(self, cell):
        row, column = cell[0], cell[1]
        current_cell = self.board[row][column]
        fired_cell_status = CellStatus.MISFIRE.value
        
        if current_cell == CellStatus.DESTROYED.value:
            fired_cell_status = CellStatus.DESTROYED.value
        
        if current_cell in (CellStatus.EMPTY.value,
                            CellStatus.NEIGHBOR.value):
            self.board[row][column] = CellStatus.MISFIRE.value
        
        if current_cell == CellStatus.SHIP.value:
            self.destroyed_ship_cells.append((row, column))
            fired_cell_status = CellStatus.DESTROYED.value
            self.board[row][column] = CellStatus.DESTROYED.value
            self.remaining_ship_cells_count -= 1
        
        return fired_cell_status
    
    def place_ship(self, cell, ship_name, ship_direction):
        if not self.is_placement_correct(cell, ship_name, ship_direction):
            return []
        
        ship_cells = self.get_ship_cells(cell, ship_name, ship_direction)
        neighbor_cells = self.get_ship_neighbor_cells(ship_cells)
        
        for nbr_cell in neighbor_cells:
            self.board[nbr_cell[0]][nbr_cell[1]] = CellStatus.NEIGHBOR.value
        for ship_cell in ship_cells:
            self.board[ship_cell[0]][ship_cell[1]] = CellStatus.SHIP.value
        for nbr_cell in neighbor_cells:
            self.neighbors_board[nbr_cell[0]][nbr_cell[1]] += 1
        
        self.non_placed_ships_count -= 1
        self.ships_remains_to_place[ship_name] -= 1
        
        ship = Ship(ship_cells, neighbor_cells, ship_name, ship_direction)
        self.ships.append(ship)
        
        return ship_cells
    
    def is_placement_correct(self, cell, ship_name, ship_direction):
        if self.ships_remains_to_place[ship_name] == 0:
            return False
        
        row = cell[0]
        column = cell[1]
        ship_range = self.ships_ranges[ship_name]
        
        if ship_direction == ShipDirection.VERTICAL.value:
            if row + ship_range[0] < self.min_cell or \
                    row + ship_range[1] > self.max_cell:
                return False
            for r in range(ship_range[0], ship_range[1] + 1):
                if self.board[row + r][column] in \
                        (CellStatus.NEIGHBOR.value,
                         CellStatus.SHIP.value):
                    return False
        
        if ship_direction == ShipDirection.HORIZONTAL.value:
            if column + ship_range[0] < self.min_cell or \
                    column + ship_range[1] > self.max_cell:
                return False
            for c in range(ship_range[0], ship_range[1] + 1):
                if self.board[row][column + c] in \
                        (CellStatus.NEIGHBOR.value,
                         CellStatus.SHIP.value):
                    return False
        
        return True
    
    def get_ship_cells(self, cell, ship_name, ship_direction):
        cells = []
        ship_range = self.ships_ranges[ship_name]
        
        if ship_direction == ShipDirection.VERTICAL.value:
            for r in range(ship_range[0], ship_range[1] + 1):
                if self.min_cell <= cell[0] + r <= self.max_cell:
                    cells.append((cell[0] + r, cell[1]))
        
        if ship_direction == ShipDirection.HORIZONTAL.value:
            for c in range(ship_range[0], ship_range[1] + 1):
                if self.min_cell <= cell[1] + c <= self.max_cell:
                    cells.append((cell[0], cell[1] + c))
        
        return cells
    
    def get_ship_neighbor_cells(self, ship_cells):
        ship_direction = get_ship_direction(ship_cells)
        neighbors = []
        
        if ship_direction == ShipDirection.VERTICAL.value:
            start_row = ship_cells[0][0] - 1
            center_column = ship_cells[0][1]
            neighbors_length = ship_cells[-1][0] - start_row + 2
            for r in range(start_row, start_row + neighbors_length):
                if self.min_cell <= r <= self.max_cell:
                    neighbors.append((r, center_column))
                    if center_column - 1 >= self.min_cell:
                        neighbors.append((r, center_column - 1))
                    if center_column + 1 <= self.max_cell:
                        neighbors.append((r, center_column + 1))
        
        if ship_direction == ShipDirection.HORIZONTAL.value:
            start_column = ship_cells[0][1] - 1
            center_row = ship_cells[0][0]
            neighbors_length = ship_cells[-1][1] - start_column + 2
            for c in range(start_column, start_column + neighbors_length):
                if self.min_cell <= c <= self.max_cell:
                    neighbors.append((center_row, c))
                    if center_row - 1 >= self.min_cell:
                        neighbors.append((center_row - 1, c))
                    if center_row + 1 <= self.max_cell:
                        neighbors.append((center_row + 1, c))
        
        return neighbors
    
    def uninit_and_get_ship_cells(self, cell):
        self.non_placed_ships_count += 1
        
        for ship in self.ships:
            for ship_cell in ship.cells:
                if ship_cell == cell:
                    cells = ship.cells
                    self.ships.remove(ship)
                    self.ships_remains_to_place[ship.name] += 1
                    self._uninit_ship(ship)
                    return cells
        return None
    
    def _uninit_ship(self, ship):
        ship_range = self.ships_ranges[ship.name]
        reset_length = abs(ship_range[0]) + ship_range[1] + 3
        
        if ship.direction == ShipDirection.VERTICAL.value:
            start_r = ship.cells[0][0] - 1
            center_c = ship.cells[0][1]
            for r in range(start_r, start_r + reset_length):
                if self.min_cell <= r <= self.max_cell:
                    self.neighbors_board[r][center_c] -= 1
                    self.board[r][center_c] = CellStatus.EMPTY.value
                    if center_c - 1 >= self.min_cell:
                        self._uninit_cell(r, center_c - 1)
                    if center_c + 1 <= self.max_cell:
                        self._uninit_cell(r, center_c + 1)
        
        if ship.direction == ShipDirection.HORIZONTAL.value:
            start_c = ship.cells[0][1] - 1
            center_r = ship.cells[0][0]
            for c in range(start_c, start_c + reset_length):
                if self.min_cell <= c <= self.max_cell:
                    self.neighbors_board[center_r][c] -= 1
                    self.board[center_r][c] = CellStatus.EMPTY.value
                    if center_r - 1 >= self.min_cell:
                        self._uninit_cell(center_r - 1, c)
                    if center_r + 1 <= self.max_cell:
                        self._uninit_cell(center_r + 1, c)
    
    def _uninit_cell(self, row, column):
        self.neighbors_board[row][column] -= 1
        if self.board[row][column] == CellStatus.SHIP.value or \
                self.neighbors_board[row][column] == 0:
            self.board[row][column] = CellStatus.EMPTY.value
    
    def check_game_status(self):
        if self.non_placed_ships_count > 0 or \
                self.opponent.non_placed_ships_count > 0:
            return GameStatus.PLACE_SHIPS.value
        
        if self.opponent.remaining_ship_cells_count == 0:
            return GameStatus.WIN.value
        
        if self.remaining_ship_cells_count == 0:
            return GameStatus.LOSE.value
        
        return GameStatus.BATTLE.value
    
    def is_ready_for_battle(self):
        if self.non_placed_ships_count > 0:
            return False
        return True
    
    def get_remains_to_place_ship_count(self, ship_name):
        return self.ships_remains_to_place[ship_name]
    
    def get_ship_name(self, cell):
        for ship in self.ships:
            for ship_cell in ship.cells:
                if ship_cell == cell:
                    return ship.name
        return None
    
    def is_ship_destroyed(self, cell):
        ship_cells = []
        for ship in self.ships:
            for ship_cell in ship.cells:
                if ship_cell == cell:
                    ship_cells = ship.cells
        
        if not ship_cells:
            return False
        
        for ship_cell in ship_cells:
            if self.board[ship_cell[0]][ship_cell[1]] == \
                    CellStatus.SHIP.value:
                return False
        
        return True
    
    def get_remaining_ship_cells(self):
        remaining_cells = []
        for ship in self.ships:
            for ship_cell in ship.cells:
                if ship_cell not in self.destroyed_ship_cells:
                    remaining_cells.append(ship_cell)
        
        return remaining_cells
