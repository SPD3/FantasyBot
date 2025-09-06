
from typing import List
from player import Player, VALID_POSITIONS
from sportsref_nfl import get_all_depth_charts
from flask import Flask, render_template
from projections import PlayerWithProjectedValue, get_player_with_projection

class PlayerWithDepth (PlayerWithProjectedValue):
    def __init__(self, name, team, position, projection, rank, bye, pos_depth):
        super().__init__(name, team, position, projection, rank, bye)
        self.pos_depth = pos_depth

available_players : List[PlayerWithDepth] = []
players_by_position = dict([(pos, []) for pos in VALID_POSITIONS])

app = Flask(__name__)

def get_name_team_pos_from_row(row):
    name=row["player"]
    team=row["team"]
    position = row["pos"]
    # Special case:
    if name.lower().strip() == "quinshon judkins":
        return ("Quinshon Judkins", "FA", "RB")
    return (name, team, position)

for i, row in get_all_depth_charts().iterrows():
    name, team, position = get_name_team_pos_from_row(row)
    if position not in VALID_POSITIONS:
        continue
    player_with_projections = get_player_with_projection(Player(
        name=name,
        team=team,
        position=position
    ))
    pos_depth=round(float(row["string"]), 2)

    if player_with_projections is not None:
        available_players.append(PlayerWithDepth(
            name=player_with_projections.name,
            team=player_with_projections.team,
            position=player_with_projections.position,
            pos_depth=pos_depth,
            projection=player_with_projections.projection,
            rank=player_with_projections.rank,
            bye=player_with_projections.bye
        ))
    else:
        available_players.append(PlayerWithDepth(
            name=row["player"],
            team=row["team"],
            position=position,
            pos_depth=pos_depth,
            projection=0.0,
            rank=0,
            bye = 0,
        ))


def update_available_players(picked_players):
    for pos in players_by_position:
        players_by_position[pos] = []

    for _ in range(len(available_players)):
        player = available_players.pop(0)
        player_picked = False
        for picked in picked_players:
            if player == picked:
                player_picked = True
                break
        
        if not player_picked:
            available_players.append(player)
    
    for available_player in available_players:
        players_by_position[available_player.position].append({
            "name" : available_player.name, 
            "team" :available_player.team, 
            "depth" : available_player.pos_depth,
            "projection" : available_player.projection,
            "rank" : available_player.rank,
            "bye" : available_player.bye
        })
    
    for position in players_by_position:
        players_by_position[position] = sorted(
            players_by_position[position], 
            key= lambda name_team_depth : (name_team_depth["projection"] - (name_team_depth["depth"] * 20)),
            reverse=True
        )

update_available_players(set())

@app.route('/')
def index():
    return render_template('index.html', data=players_by_position)

if __name__ == "__main__":
    for player in available_players:
        if player.name == "Tony Pollard":
            print(player.name)
            print(player.position)
            print(player.team)
            print(player.bye)
            print(player.pos_depth)
            print(player.projection)
            print(player.rank)
