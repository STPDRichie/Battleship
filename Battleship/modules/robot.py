from random import randint

from modules.player import Player

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

ship_list = ['Battleship', 'Cruiser', 'Submarine', 'Destroyer']
directions = ['Vertical', 'Horizontal']


class Robot(Player):
    def __init__(self):
        super().__init__()
        self.opponent_empty_cells = []
        for i in range(1, 11):
            for j in range(1, 11):
                self.opponent_empty_cells.append([i, j])
        self.last_fired_cell = []

    def init_board(self):
        while self.non_placed_ships_count > 0:
            ship = ship_list[randint(0, 3)]
            while self.ships_remains_to_place[ship] == 0:
                ship = ship_list[randint(0, 3)]

            column, row = randint(1, 10), randint(1, 10)
            ship_direction = directions[randint(0, 1)]
            while not self.is_placement_correct(
                    [column, row], ship, ship_direction):
                column, row = randint(1, 10), randint(1, 10)
                ship_direction = directions[randint(0, 1)]

            self.place_ship([column, row], ship, ship_direction)

    def random_fire(self):
        column, row = randint(1, 10), randint(1, 10)
        while [column, row] not in self.opponent_empty_cells:
            column, row = randint(1, 10), randint(1, 10)

        fire_result, one_more = self.opponent.get_fired([column, row])
        self.opponent_empty_cells.remove([column, row])

        if fire_result == cell_destroyed:
            if one_more:
                self.opponent_remaining_ship_cells_count -= 1
            if self.opponent_remaining_ship_cells_count == 0:
                return status_lose, [column, row], cell_destroyed
            return status_battle, [column, row], cell_destroyed

        if fire_result == cell_missfire:
            return status_battle, [column, row], cell_missfire
