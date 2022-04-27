from enum import Enum


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
