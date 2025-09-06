
TEAM_ABBR_MAPPING = {
    "ARI": "ARI", "ARZ": "ARI", "CRD" : "ARI",
    "ATL": "ATL",
    "BAL": "BAL", "RAV" : "BAL",
    "BUF": "BUF",
    "CAR": "CAR",
    "CHI": "CHI",
    "CIN": "CIN",
    "CLE": "CLE",
    "DAL": "DAL",
    "DEN": "DEN",
    "DET": "DET",
    "GB": "GB", "GNB": "GB",
    "HOU": "HOU", "HTX" : "HOU",
    "IND": "IND", "CLT" : "IND",
    "JAX": "JAX", "JAC": "JAX",
    "KC": "KC", "KCC": "KC", "KAN" : "KC",
    "LV": "LV", "OAK": "LV", "RAI": "LV", "LVR" : "LV",
    "LAC": "LAC", "SD": "LAC", "SDC": "LAC", "SDG" : "LAC",
    "LAR": "LAR", "STL": "LAR", "RAM" : "LAR",
    "MIA": "MIA",
    "MIN": "MIN",
    "NE": "NE", "NWE": "NE",
    "NO": "NO", "NOR": "NO",
    "NYG": "NYG", "NYGHT": "NYG",
    "NYJ": "NYJ",
    "PHI": "PHI",
    "PIT": "PIT",
    "SF": "SF", "SFO": "SF",
    "SEA": "SEA",
    "TB": "TB", "TAM": "TB", "TBB": "TB",
    "TEN": "TEN", "OTI": "TEN",
    "WAS": "WAS", "WSH": "WAS", "WFT": "WAS", "RED": "WAS",
    "FA" : "FA",
}

VALID_POSITIONS = {
    "WR" : "WR",
    "WRCB" : "WR",
    "RB" : "RB",
    "QB" : "QB",
    "TE" : "TE",
}

def standardize_team_abbreviation(abbr: str) -> str:
    """
    Standardize NFL three-letter team abbreviations.
    Input can be any known variation, output will be the official NFL abbreviation.
    """
    return TEAM_ABBR_MAPPING[abbr.strip().upper()]

def standardize_name(name:str) -> str:
    name = name.lower()
    for suff in ["jr", "jr.", "sr", "sr.", "iii"]:
        name = name.removesuffix(suff)
    name = name.replace(".", "")
    name = name.strip()
    # Special Cases:
    if name == "marquise brown":
        name = "hollywood brown"

    return name.title()

class Player:
    def __init__(self, name, team, position):
        self.name = standardize_name(name)
        self.team = standardize_team_abbreviation(team)
        self.position = position

    def __str__(self):
        return f"{self.name}-{self.team}-{self.position}"
    
    def __eq__(self, value):
        def cmp(s1, s2):
            return str(s1).lower()== str(s2).lower()
        return isinstance(value, Player) and cmp(self.name, value.name) and cmp(self.team, value.team) and cmp(self.position, value.position)
    
    def __hash__(self):
        return hash(f"{str(self.name).lower()}_{str(self.team).lower()}_{str(self.position.lower())}")