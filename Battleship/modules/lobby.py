class Lobby:
    def __init__(self, session_key, player1_name, player2_name=None):
        self.session_key = session_key
        self.player1_name = player1_name
        self.player2_name = player2_name

    def init_second_player(self, player2_name):
        self.player2_name = player2_name
