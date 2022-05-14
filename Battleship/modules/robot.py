import time
from random import randint, uniform

from modules.domain import CellStatus, ShipName, ShipDirection
from modules.player import Player

ship_list = [ShipName.BATTLESHIP.value, ShipName.CRUISER.value,
             ShipName.SUBMARINE.value, ShipName.DESTROYER.value]

directions = [ShipDirection.VERTICAL.value, ShipDirection.HORIZONTAL.value]


class Robot(Player):
    def __init__(self, board_data):
        super().__init__(board_data)
        self.diff_ships_count = board_data.get_different_ships_count()
        
        self.opponent_not_empty_cells = set()
        
        self.next_cells_to_fire = []
        self.last_destroyed_cell = None
    
    def init_board(self):
        while self.non_placed_ships_count > 0:
            ship = ship_list[randint(0, self.diff_ships_count - 1)]
            while self.ships_remains_to_place[ship] == 0:
                ship = ship_list[randint(0, self.diff_ships_count - 1)]
            
            row = randint(0, self.board_size - 1)
            column = randint(0, self.board_size - 1)
            ship_direction = directions[randint(0, 1)]
            while not self.is_placement_correct((row, column),
                                                ship, ship_direction):
                row = randint(0, self.board_size - 1)
                column = randint(0, self.board_size - 1)
                ship_direction = directions[randint(0, 1)]
            
            self.place_ship((row, column), ship, ship_direction)
    
    def random_fire(self):
        next_cells_length = len(self.next_cells_to_fire)
        if next_cells_length != 0:
            cell = self.next_cells_to_fire[randint(0, next_cells_length - 1)]
            self.next_cells_to_fire.remove(cell)
        else:
            cell = (randint(0, self.board_size - 1),
                    randint(0, self.board_size - 1))
            while cell in self.opponent_not_empty_cells:
                cell = (randint(0, self.board_size - 1),
                        randint(0, self.board_size - 1))
        
        time.sleep(round(uniform(0.5, 1.5), 1))
        fired_cell_status = self.opponent.get_fired(cell)
        self.opponent_not_empty_cells.add(cell)
        
        if fired_cell_status == CellStatus.DESTROYED.value:
            self.update_cells_to_fire_by_destroyed(cell)
            self.last_destroyed_cell = cell
        
        if self.opponent.is_ship_destroyed(cell):
            for next_cell in self.next_cells_to_fire:
                self.opponent_not_empty_cells.add(next_cell)
            self.next_cells_to_fire.clear()
            self.last_destroyed_cell = None
        
        return cell, fired_cell_status
    
    def update_cells_to_fire_by_destroyed(self, cell):
        cell_neighbors = []
        for row in range(-1, 2):
            for column in range(-1, 2):
                if self.min_cell <= row + cell[0] <= self.max_cell and \
                        self.min_cell <= column + cell[1] <= self.max_cell:
                    if (row + column) % 2 != 0:
                        cell_neighbors.append(
                            (row + cell[0], column + cell[1]))
                    else:
                        self.opponent_not_empty_cells.add(
                            (row + cell[0], column + cell[1]))
        
        next_cells = self.get_empty_cells_from_neighbors(cell_neighbors)
        self.next_cells_to_fire.extend(next_cells)
        self.refine_next_cells_to_fire(cell)
    
    def get_empty_cells_from_neighbors(self, neighbors):
        cells = []
        for cell in neighbors:
            if cell not in self.opponent_not_empty_cells:
                cells.append(cell)
        
        return cells
    
    def refine_next_cells_to_fire(self, cell):
        if not self.last_destroyed_cell:
            return
        
        if cell[0] == self.last_destroyed_cell[0]:
            self._refine_next_cells_by_direction(cell, 0)
        else:
            self._refine_next_cells_by_direction(cell, 1)
    
    def _refine_next_cells_by_direction(self, cell, dir_index):
        next_cells = self.next_cells_to_fire.copy()
        for next_cell in next_cells:
            if next_cell == self.last_destroyed_cell:
                self.next_cells_to_fire.remove(next_cell)
            
            if next_cell[dir_index] != cell[dir_index]:
                self.next_cells_to_fire.remove(next_cell)
                self.opponent_not_empty_cells.add(next_cell)
