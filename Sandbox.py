
from player import Player
from sportsref_nfl import get_all_depth_charts

VALID_POSITIONS = set([
    "WR","RB","QB","TE",
])

class PlayerWithDepth (Player):
    def __init__(self, name, team, position, pos_depth):
        super().__init__(name, team, position)
        self.pos_depth = pos_depth

    def __hash__(self):
        return hash(str(self) + str(self.pos_depth))

available_players = []

for i, row in get_all_depth_charts():
    position = row["pos"]
    if position not in VALID_POSITIONS:
        continue
    available_players.append(PlayerWithDepth(
        name=row["player"],
        team=row["team"],
        position=position,
        pos_depth=row["string"]
    ))

def update_available_players(picked_players):
    ...