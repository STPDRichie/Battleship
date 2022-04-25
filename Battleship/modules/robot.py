from random import randint

from modules.player import Player

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

ship_list = ['Battleship', 'Cruiser', 'Submarine', 'Destroyer']
directions = ['Vertical', 'Horizontal']


class Robot(Player):
    def __init__(self):
        super().__init__()
        self.opponent_not_empty_cells = set()

        self.next_cells_to_fire = []
        self.last_destroyed_cell = None

    def init_board(self):
        while self.non_placed_ships_count > 0:
            ship = ship_list[randint(0, 3)]
            while self.ships_remains_to_place[ship] == 0:
                ship = ship_list[randint(0, 3)]

            row, column = randint(0, 9), randint(0, 9)
            ship_direction = directions[randint(0, 1)]
            while not self.is_placement_correct((row, column),
                                                ship, ship_direction):
                row, column = randint(0, 9), randint(0, 9)
                ship_direction = directions[randint(0, 1)]

            self.place_ship((row, column), ship, ship_direction)

    def random_fire(self):
        next_cells_length = len(self.next_cells_to_fire)
        if next_cells_length != 0:
            cell = self.next_cells_to_fire[randint(0, next_cells_length - 1)]
            self.next_cells_to_fire.remove(cell)
        else:
            cell = (randint(0, 9), randint(0, 9))
            while cell in self.opponent_not_empty_cells:
                cell = (randint(0, 9), randint(0, 9))

        fired_cell_status, is_one_more = self.opponent.get_fired(cell)
        self.opponent_not_empty_cells.add(cell)

        if fired_cell_status == cell_destroyed:
            self.update_cells_to_fire_by_destroyed(cell)
            self.last_destroyed_cell = cell
            if is_one_more:
                self.opponent_remaining_ship_cells_count -= 1

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
                if 0 <= row + cell[0] <= 9 and 0 <= column + cell[1] <= 9:
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
