from dataclasses import dataclass


@dataclass(frozen=True)
class Turn:
    player_name: str
    fired_cell: ()
    # def __init__(self, player_name, fired_cell):
    #     self.player_name = player_name
    #     self.fired_cell = fired_cell
