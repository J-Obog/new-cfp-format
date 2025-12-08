from dataclasses import dataclass
from common import get_soup_from_file

SCHOOL_OPTIONS_FILENAME = "files/sim/sim_school_options.html"

SchoolName = str
SchoolId = str

@dataclass
class SimResult:
    pass

class SimUtils:
    @staticmethod
    def sim_game(year: int, team_a: str, team_b: str):
        pass

    @staticmethod
    def get_sim_school_to_id_map() -> dict[SchoolName, SchoolId]:
        soup = get_soup_from_file(SCHOOL_OPTIONS_FILENAME)

        data_map = {}
        for option in soup.find_all("option"):
            if option.has_attr("value"):
                data_map[option.text] = option["value"]
        
        return data_map
