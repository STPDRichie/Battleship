class Ship:
    def __init__(self, cells, neighbor_cells, name, direction):
        self.cells = cells
        self.neighbor_cells = neighbor_cells
        self.name = name
        self.direction = direction
