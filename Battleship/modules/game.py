from random import choice

from modules.lobby import Lobby
from modules.player import Player
from modules.robot import Robot
from modules.domain import BoardData


class Game:
    def __init__(self, lobby: Lobby, board_data: BoardData):
        self.lobby = lobby
        self.board_data = board_data
        
        self.player1: Player = Player(board_data)
        if not lobby.member_name:
            self.player2 = Robot(board_data)
            self.player2.init_board()
        else:
            self.player2 = Player(board_data)
        self.player1.init_opponent(self.player2)
        self.player2.init_opponent(self.player1)
        
        self.is_battle_started = False
        self.whose_turn = choice([lobby.host_name, lobby.member_name])
        self.last_turn = None
    
    def change_turn_player(self):
        if self.whose_turn == self.lobby.host_name:
            self.whose_turn = self.lobby.member_name
        else:
            self.whose_turn = self.lobby.host_name
    
    def change_last_turn(self, turn):
        self.last_turn = turn
