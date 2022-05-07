from modules.player import Player
from modules.robot import Robot


class Game:
    def __init__(self, lobby):
        self.lobby = lobby

        self.player1 = Player()
        if not lobby.player2_name:
            self.player2 = Robot()
            self.player2.init_board()
        else:
            self.player2 = Player()
        self.player1.init_opponent(self.player2)
        self.player2.init_opponent(self.player1)
