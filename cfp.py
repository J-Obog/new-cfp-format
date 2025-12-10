from dataclasses import dataclass
from typing import List
from sportsref import SportsrefUtil


@dataclass
class PlayoffSeed:
    seed: int
    team: str
    is_conf_champ: bool

def get_playoff_seeds(year: int) -> List[PlayoffSeed]:
    conf_champs = SportsrefUtil.get_conference_champions(year)
    playoff_teams = conf_champs
    team_to_rating = {}
    team_to_cfp_ranking = {} 

    cfp_rankings = SportsrefUtil.get_final_cfp_rankings(year)
    
    for cfp_rank in cfp_rankings:
        team_to_cfp_ranking[cfp_rank.school] = cfp_rank.rank

    for team_rating in SportsrefUtil.get_team_ratings(year):
        team_to_rating[team_rating.school] = team_rating.rating

    pp = list(filter(lambda r: r.school not in playoff_teams, sorted(cfp_rankings, key=lambda x: x.rank)))
    sss = list(map(lambda x: x.school, pp))

    playoff_teams.extend(sss)
    playoff_teams = playoff_teams[:16]

    team_eff_rank_list = []

    for team in playoff_teams:
        eff_rank = team_to_cfp_ranking[team] if team in team_to_cfp_ranking else team_to_rating[team]
        team_eff_rank_list.append({"eff_rank": eff_rank, "tm": team})

    tms = [] 

    for i,team in enumerate(sorted(team_eff_rank_list, key=lambda x: x["eff_rank"])):
        tms.append(
            PlayoffSeed(i + 1, team["tm"], team["tm"] in conf_champs)
        )
    return tms



for i in range(2014, 2025):
    print("----------Year----------", i)
    for t in get_playoff_seeds(i):
        print(t.seed, t.team)

#print(SportsrefUtil.get_final_cfp_rankings(2024))
#print(SportsrefUtil.get_conference_champions(2024))