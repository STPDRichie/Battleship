from modules.player import Player
from modules.robot import Robot


class Game:
    def __init__(self, session_key, player1_name, player2_name=None):
        self.key = session_key
        self.player1_name = player1_name
        self.player2_name = player2_name

        self.player1 = Player()
        if not player2_name:
            self.player2 = Robot()
            self.player2.init_board()
        else:
            self.player2 = Player()
        self.player1.init_opponent(self.player2)
        self.player2.init_opponent(self.player1)
