import json

from sim import SimUtils
from sportsref import SportsrefUtil 

MAPPING_OUTPUT_FILENAME = "sportsref_to_sim_id.json"

sim_school_to_id_map = SimUtils.get_sim_school_to_id_map()
sportsref_cfb_schools = SportsrefUtil.get_sportsref_active_schools()

SPECIAL_MAPPINGS = {
    "Florida International": "FIU", 
    "Louisiana-Monroe": "UL Monroe",
    "Miami (FL)": "Miami", 
    "Miami (OH)": "Miami (Ohio)",
    "Middle Tennessee State": "Middle Tennessee",
    "Nevada-Las Vegas": "UNLV",
    "North Carolina": "UNC",
    "North Carolina State": "NC State",
    "Pitt": "Pittsburgh",
    "South Florida": "USF",
    "Southern Mississippi": "Southern Miss",
    "Texas Christian": "TCU", 
    "UTSA": "TX-San Antonio"
}

sportsref_to_sim_id_map = {}

for school in sportsref_cfb_schools:
    sim_school = school if school in sim_school_to_id_map else SPECIAL_MAPPINGS[school]
    sportsref_to_sim_id_map[school] = sim_school_to_id_map[sim_school]
    
with open(MAPPING_OUTPUT_FILENAME, "w+", encoding="utf-8") as outfile:
    json.dump(sportsref_to_sim_id_map, outfile)