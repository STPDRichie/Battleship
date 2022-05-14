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
    _min_cell_index: int = 0,
    _max_cell_index: int = 9,
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
    
    def get_min_cell_index(self):
        return self._min_cell_index
    
    def get_max_cell_index(self):
        return self._max_cell_index
    
    def convert_column(self, column):
        return self._column_numbers_and_letters[column]


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
