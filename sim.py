from dataclasses import dataclass
from typing import List
from common import get_soup_from_file, get_soup_from_html
import requests

SCHOOL_OPTIONS_FILENAME = "files/sim/sim_school_options.html"

SchoolName = str
SchoolId = str

@dataclass
class TeamScore:
    team_id: str
    score: int

@dataclass
class SimResult:
    scores: List[TeamScore]
    winner: str

class SimUtils:
    @staticmethod
    def sim_game(year: int, team_a: str, team_b: str):
        payload = {
            "HomeTeam": team_a, 
            "HomeYear": year + 1, 
            "AwayTeam": team_b, 
            "AwayYear": year + 1, 
            "hs": 1
        }
        data = requests.post("https://www.mygamesim.com/cfb/fb_gamesimulator.asp", data=payload)        
        soup = get_soup_from_html(data.text)
        scores = list(map(lambda x: int(x.text.strip()), soup.find_all("div", class_="col-xs-12 gs_score")))

        team_a_score = TeamScore(team_a, scores[0])
        team_b_score = TeamScore(team_b, scores[1])
        
        winner = team_a if team_a_score.score > team_b_score.score else team_b

        return SimResult([team_a_score, team_b_score], winner)


    @staticmethod
    def get_sim_school_to_id_map() -> dict[SchoolName, SchoolId]:
        soup = get_soup_from_file(SCHOOL_OPTIONS_FILENAME)

        data_map = {}
        for option in soup.find_all("option"):
            if option.has_attr("value"):
                data_map[option.text] = option["value"]
        
        return data_map
