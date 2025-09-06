from typing import List, Optional
from player import Player

class PlayerWithProjectedValue (Player):
    def __init__(self, name, team, position, projection, rank, bye):
        super().__init__(name, team, position)
        self.projection = projection
        self.rank = rank
        self.bye = bye

def _parse_player_projections():
    with open("Projections.txt", "r") as f:
        lines = [line.removesuffix("\n") for line in f]

    player_projections = set()
    for i in range(12, len(lines), 10):
        projections = str(lines[i+7]).split()
        proj_1 = int(projections[0])
        proj_2 = int(projections[1])
        proj_avg = int((proj_1 + proj_2) / 2)
        player_projections.add(
            PlayerWithProjectedValue(
                name=lines[i + 1],
                team=lines[i+2],
                position=str(lines[i+3])[:2],
                projection=proj_avg,
                rank=int(lines[i]),
                bye=int(lines[i+5].split()[2])
            )
        )

    return player_projections

players_with_projections = _parse_player_projections()

def get_player_with_projection(player) -> Optional[PlayerWithProjectedValue]:
    for p in players_with_projections:
        if p == player:
            return p