import random
import time

import app

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


class Robot:
    def __init__(self):
        self.opponent_empty_cells = []
        for i in range(1, 11):
            for j in range(1, 11):
                self.opponent_empty_cells.append([i, j])
        self.last_fired_cell = []
        self.init_board()

    def init_board(self):
        app.opponent.place_ship([1, 2], 'Battleship', 'Vertical')
        app.opponent.place_ship([3, 2], 'Cruiser', 'Vertical')
        app.opponent.place_ship([5, 2], 'Cruiser', 'Vertical')
        app.opponent.place_ship([7, 1], 'Submarine', 'Vertical')
        app.opponent.place_ship([9, 1], 'Submarine', 'Vertical')
        app.opponent.place_ship([1, 6], 'Submarine', 'Vertical')
        app.opponent.place_ship([3, 6], 'Destroyer', 'Vertical')
        app.opponent.place_ship([5, 6], 'Destroyer', 'Vertical')
        app.opponent.place_ship([7, 6], 'Destroyer', 'Vertical')
        app.opponent.place_ship([9, 6], 'Destroyer', 'Vertical')
        print(app.opponent.ships)
        for i in range(10):
            print(app.opponent.neighbors_board[i])

    def fire(self):
        column = random.randint(1, 10)
        row = random.randint(1, 10)
        while [column, row] not in self.opponent_empty_cells:
            column = random.randint(1, 10)
            row = random.randint(1, 10)
        fire_result, one_more = app.person.get_fired([column, row])
        self.opponent_empty_cells.remove([column, row])
        if fire_result == cell_destroyed:
            if one_more:
                app.opponent.opponent_remaining_ship_cells_count -= 1
            if app.opponent.opponent_remaining_ship_cells_count == 0:
                return status_lose, [column, row], cell_destroyed
            return status_battle, [column, row], cell_destroyed
        if fire_result == cell_missfire:
            return status_battle, [column, row], cell_missfire
