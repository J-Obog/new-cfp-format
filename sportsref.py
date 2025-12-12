from typing import List
from bidir import BidirMap
from common import get_soup_from_file

CFB_SCHOOLS_FILENAME = "files/sportsref/cfb_schools.xls"

SchoolName = str 
Ranking = int

class SportsrefUtil:
    @staticmethod
    def get_team_ratings(year: int) -> SchoolName, Ranking:
        soup = get_soup_from_file(f"files/sportsref/team_ratings/rat_{year}.xls")
        ratings = {}

        for row in soup.find_all("tr"):
            if row.has_attr("data-row"):
                rating = int(row.find("th", attrs={"data-stat": "ranker"}).text)
                team = row.find("td", attrs={"data-stat": "school_name"}).text
                ratings[team] = rating

        return ratings
    
    @staticmethod
    def get_conference_champions(year: int) -> List[str]:
        soup = get_soup_from_file(f"files/sportsref/conferences/conf_{year}.xls")

        champs = []
        for row in soup.find_all("tr"):
            if row.has_attr("data-row"):
                team = row.find("td", attrs={"data-stat": "conf_champ"}).text.strip()
                
                if team == "":
                    continue

                if "," in team:
                    champs.extend(list(map(lambda x: x.strip(), team.split(","))))
                else:
                    champs.append(team)

        return champs

    @staticmethod
    def get_final_cfp_rankings(year: int) -> dict[SchoolName, Ranking]:
        soup = get_soup_from_file(f"files/sportsref/cfp_rankings/cfp_{year}.xls")
        rankings = {}

        for row in soup.find_all("tr"):
            if row.has_attr("data-row"):
                poll_date = row.find("td", attrs={"data-stat": "date_poll"}).text
                
                if poll_date != "Final":
                    continue

                rank = int(row.find("td", attrs={"data-stat": "rank"})["csk"].split(".")[0])
                school = row.find("td", attrs={"data-stat": "school_name"})["csk"].split(".")[0]
                rankings[school] = rank

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
    