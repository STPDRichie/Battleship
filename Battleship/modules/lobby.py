class Lobby:
    def __init__(self, session_key, host_name, member_name=None):
        self.session_key = session_key
        self.host_name = host_name
        self.member_name = member_name
        self.is_game_started = False
    
    def init_second_player(self, member_name):
        self.member_name = member_name
    
    def uninit_second_player(self):
        self.member_name = None
