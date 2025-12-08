from dataclasses import dataclass
from common import get_soup_from_file
import requests

SCHOOL_OPTIONS_FILENAME = "files/sim/sim_school_options.html"

SchoolName = str
SchoolId = str

@dataclass
class SimResult:
    pass

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
        

    @staticmethod
    def get_sim_school_to_id_map() -> dict[SchoolName, SchoolId]:
        soup = get_soup_from_file(SCHOOL_OPTIONS_FILENAME)

        data_map = {}
        for option in soup.find_all("option"):
            if option.has_attr("value"):
                data_map[option.text] = option["value"]
        
        return data_map
