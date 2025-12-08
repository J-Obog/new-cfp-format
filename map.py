from typing import List
from bs4 import BeautifulSoup
import json 

def get_soup_from_file(filename: str) -> BeautifulSoup:
    with open(filename, "r") as f:
        return BeautifulSoup(f.read(), 'html.parser')

def get_sim_school_to_id_map() -> dict[str, str]:
    soup = get_soup_from_file("sim_school_options.html")

    data_map = {}
    for option in soup.find_all("option"):
        if option.has_attr("value"):
            data_map[option.text] = option["value"]
    
    return data_map

def get_sportsref_active_schools() -> List[str]:
    soup = get_soup_from_file("cfb_schools.xls")

    schools = []

    for row in soup.find_all("tr"):
        if row.has_attr("data-row"):
            max_year = row.find("td", attrs={"data-stat": "year_max"}).text
            
            if max_year != "2025":
                continue

            schools.append(row.find("td", attrs={"data-stat": "school_name"}).text)

    return schools


sim_school_to_id_map = get_sim_school_to_id_map()
sportsref_cfb_schools = get_sportsref_active_schools()

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
    
with open("sportsref_to_sim_id.json", "w+", encoding="utf-8") as outfile:
    json.dump(sportsref_to_sim_id_map, outfile)