from dataclasses import dataclass
from typing import List, Optional
from sim import SimResult
from sportsref import SportsrefUtil
import json
from sim import SimUtils


@dataclass
class PlayoffSeed:
    seed: int
    team: str
    is_conf_champ: bool

@dataclass
class PlayoffMatchup:
    round: int
    position: int
    team_a: str
    team_b: str
    result: Optional[SimResult]

@dataclass
class PlayoffBracket:
    seeds: List[PlayoffSeed]
    matchups: List[PlayoffMatchup]

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

sim_school_id_map = {}

with open("sportsref_to_sim_id.json", "r", encoding="utf-8") as ff:
    sim_school_id_map = json.load(ff)

sref_from_if_map = {}

for k in sim_school_id_map:
    sref_from_if_map[sim_school_id_map[k]] = k

t_year = 2024

seeds = get_playoff_seeds(t_year)

print(seeds)

seed_to_team = {}
team_to_seed = {}
for tm in seeds:
    team_to_seed[tm.team] = tm.seed
    seed_to_team[tm.seed] = tm.team

last_round: List[PlayoffMatchup] = []
champion = None

for n,pair in enumerate([(1,16),(8,9),(5,12),(4,13),(6,11),(3, 14),(7, 10),(2,15)]):
    pm = PlayoffMatchup(1, n+1, seed_to_team[pair[0]], seed_to_team[pair[1]], None)
    last_round.append(pm)




while len(last_round) >= 1:
    if len(last_round) == 1:
        pass

    new_round = []

    for i in range(len(last_round)):
        mm = last_round[i]
        team_a_id = sim_school_id_map[mm.team_a]
        team_b_id = sim_school_id_map[mm.team_b]

        res = SimUtils.sim_game(t_year, team_a_id, team_b_id)

        last_round[i].result = res
    

    next_round_id = last_round[-1].round + 1

    n_round = []

    for n in range(1, len(last_round),2):
        winner1 = sref_from_if_map[last_round[n-1].result.winner]
        winner2 = sref_from_if_map[last_round[n].result.winner]
        
        pos = len(n_round) + 1

        n_round.append(PlayoffMatchup(next_round_id, pos, winner1, winner2, None))

    #last_round = n_round
    print(n_round)

    #print(last_round)
    break