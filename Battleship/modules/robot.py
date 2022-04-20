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
        self.opponent_empty_cells = []
        for i in range(10):
            for j in range(10):
                self.opponent_empty_cells.append([i, j])

    def init_board(self):
        while self.non_placed_ships_count > 0:
            ship = ship_list[randint(0, 3)]
            while self.ships_remains_to_place[ship] == 0:
                ship = ship_list[randint(0, 3)]

            row, column = randint(0, 9), randint(0, 9)
            ship_direction = directions[randint(0, 1)]
            while not self.is_placement_correct([row, column],
                                                ship, ship_direction):
                row, column = randint(0, 9), randint(0, 9)
                ship_direction = directions[randint(0, 1)]

            self.place_ship([row, column], ship, ship_direction)

    def random_fire(self):
        cell = [randint(0, 9), randint(0, 9)]
        while cell not in self.opponent_empty_cells:
            cell = [randint(0, 9), randint(0, 9)]

        fired_cell_status, is_one_more = self.opponent.get_fired(cell)
        self.opponent_empty_cells.remove(cell)

        if fired_cell_status == cell_destroyed and is_one_more:
            self.opponent_remaining_ship_cells_count -= 1

        return cell, fired_cell_status
