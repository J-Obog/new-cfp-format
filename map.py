from typing import List
from bs4 import BeautifulSoup


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


for school in sportsref_cfb_schools:
    if school not in sim_school_to_id_map:
        print(school)