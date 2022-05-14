from enum import Enum
from dataclasses import dataclass, field


class GameStatus(Enum):
    START = 'Start game'
    PLACE_SHIPS = 'Ships placing'
    BATTLE = 'Battle'
    WIN = 'Win'
    LOSE = 'Lose'


class ShipName(Enum):
    BATTLESHIP = 'Battleship'
    CRUISER = 'Cruiser'
    SUBMARINE = 'Submarine'
    DESTROYER = 'Destroyer'


class ShipDirection(Enum):
    VERTICAL = 'Vertical'
    HORIZONTAL = 'Horizontal'


class CellStatus(Enum):
    EMPTY = 'Empty'
    SHIP = 'Ship'
    NEIGHBOR = 'Neighbor'
    MISFIRE = 'Misfire'
    DESTROYED = 'Destroyed'


class CellIcon(Enum):
    EMPTY = '<i class="fa-solid"></i>'
    SHIP = '<i class="fa-solid fa-circle"></i>'
    MISFIRE = '<i class="fa-regular fa-circle"></i>'
    DESTROYED = '<i class="fa-solid fa-circle-xmark"></i>'


class PlayerName(Enum):
    PERSON = 'person'
    OPPONENT = 'opponent'


@dataclass(frozen=True)
class Board10:
    _board_size: int = 10
    _min_cell_index: int = 0
    _max_cell_index: int = 9
    _column_numbers_and_letters: dict = \
        field(default_factory=lambda: ({
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
        }))
    _different_ships_count: int = 4
    _ship_cells_count: int = 20
    _non_placed_ships_count: int = 10
    _ships_remains_to_place: dict = \
        field(default_factory=lambda: ({
            'Battleship': 1,
            'Cruiser': 2,
            'Submarine': 3,
            'Destroyer': 4
        }))
    
    def get_board_size(self):
        return int(self._board_size)
    
    def get_min_cell_index(self):
        return int(self._min_cell_index)
    
    def get_max_cell_index(self):
        return int(self._max_cell_index)
    
    def convert_column(self, column):
        return self._column_numbers_and_letters[column]
    
    def get_different_ships_count(self):
        return int(self._different_ships_count)
    
    def get_ship_cells_count(self):
        return int(self._ship_cells_count)
    
    def get_non_placed_ships_count(self):
        return int(self._non_placed_ships_count)
    
    def get_ships_remains_to_place(self):
        return dict(self._ships_remains_to_place)


@dataclass(frozen=True)
class GameChange:
    is_lobby_exist: bool = False
    is_changed: bool = False
    is_game_restarted: bool = False
    whose_turn: str = None
    game_status: str = GameStatus.START.value
    cells: list = field(default_factory=list)
    icon: str = CellIcon.EMPTY.value
    is_ship_destroyed: bool = False
    destroyed_ship: str = ''
    ship_count: int = 0
    returned_ship: str = ''
    is_person_ready_for_battle: bool = False
    is_opponent_ready_for_battle: bool = False


@dataclass(frozen=True)
class LobbyChange:
    is_lobby_exist: bool = False
    is_changed: bool = False
    whose_turn: str = None
    opponent: str = None
