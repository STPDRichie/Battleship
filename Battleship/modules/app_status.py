import app
from modules.game import Game
from modules.lobby import Lobby
from modules.domain import PlayerName, Board10

board_data = Board10()


def get_lobby_if_exist(session_key) -> Lobby:
    current_lobby = next((lobby for lobby in app.lobbies
                          if lobby.session_key == session_key), None)
    return current_lobby


def get_game_if_exist(session_key) -> Game:
    current_game = next((game for game in app.games
                         if game.lobby.session_key == session_key), None)
    return current_game


def cells_to_other_player_id_format(cells_ids):
    if not cells_ids or not cells_ids[0]:
        return None
    
    cells = []
    for cell_id in cells_ids:
        cells.append(convert_cell_id_to_computing_format(cell_id))
    
    if cells_ids[0].split('-')[0] == PlayerName.OPPONENT.value:
        return convert_player_cells_to_id(cells, PlayerName.PERSON.value)
    return convert_player_cells_to_id(cells, PlayerName.OPPONENT.value)


def convert_cell_id_to_computing_format(cell_id):
    column, row = cell_id.split('_')[-1].split('-')
    column = int(board_data.convert_column(column)) - 1
    row = int(row) - 1
    return row, column


def convert_player_cells_to_id(cells, player):
    cells_ids = []
    for cell in cells:
        cells_ids.append(
            f'{player}-board__cell_'
            f'{board_data.convert_column(cell[1] + 1)}-'
            f'{cell[0] + 1}'
        )
    
    return cells_ids
