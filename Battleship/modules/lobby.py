class Lobby:
    def __init__(self, session_key, host_name, member_name=None):
        self.session_key = session_key
        self.host_name = host_name
        self.member_name = member_name
        self.is_game_started = False

    def init_second_player(self, player2_name):
        self.member_name = player2_name

    def uninit_second_player(self):
        self.member_name = None

    def __str__(self):
        return f'{self.session_key}: ' \
               f'HOST IS {self.host_name}, MEMBER IS {self.member_name}'
