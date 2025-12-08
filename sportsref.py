from typing import List
from common import get_soup_from_file

CFB_SCHOOLS_FILENAME = "cfb_schools.xls"

class SportsrefUtil:
    @staticmethod
    def get_sportsref_active_schools() -> List[str]:
        soup = get_soup_from_file(CFB_SCHOOLS_FILENAME)

        schools = []

        for row in soup.find_all("tr"):
            if row.has_attr("data-row"):
                max_year = row.find("td", attrs={"data-stat": "year_max"}).text
                
                if max_year != "2025":
                    continue

                schools.append(row.find("td", attrs={"data-stat": "school_name"}).text)

        return schools
    