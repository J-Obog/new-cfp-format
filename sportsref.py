from typing import List
from common import get_soup_from_file
from dataclasses import dataclass

CFB_SCHOOLS_FILENAME = "files/sportsref/cfb_schools.xls"

@dataclass
class CfpRanking:
    rank: int
    school: str

@dataclass
class TeamRatingRanking:
    rank: int
    school: str

class SportsrefUtil:
    @staticmethod
    def get_final_cfp_rankings(year: int) -> List[CfpRanking]:
        soup = get_soup_from_file(f"files/sportsref/cfp_rankings/cfp_{year}.xls")

        rankings = []
        for row in soup.find_all("tr"):
            if row.has_attr("data-row"):
                poll_date = row.find("td", attrs={"data-stat": "date_poll"}).text
                
                if poll_date != "Final":
                    continue

                rank = int(row.find("td", attrs={"data-stat": "rank"})["csk"].split(".")[0])
                school = row.find("td", attrs={"data-stat": "school_name"})["csk"].split(".")[0]
                rankings.append(
                    CfpRanking(rank=rank, school=school)
                )

        return rankings

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
    