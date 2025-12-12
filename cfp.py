from dataclasses import dataclass
from typing import List, Optional
from sim import SimResult
from sportsref import SportsrefUtil
import json
from sim import SimUtils
from bidict import bidict


@dataclass
class PlayoffMetadata:
    conf_champs: List[str]
    seeds: bidict[str, int]

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


def get_playoff_metadata(year: int) -> PlayoffMetadata:
    conf_champs = SportsrefUtil.get_conference_champions(year)
    team_to_ovr_ranking = SportsrefUtil.get_team_ratings(year)
    team_to_cfp_ranking = bidict(SportsrefUtil.get_final_cfp_rankings(year))
    playoff_teams = conf_champs

    candidate_seed = 1
    while len(playoff_teams) != 16:
        team = team_to_cfp_ranking.inverse[candidate_seed]
        candidate_seed += 1
        if team in playoff_teams:
            continue

        playoff_teams.append(team)

    
    eff_rank_fn = lambda team: team_to_cfp_ranking[team] if team in team_to_cfp_ranking else team_to_ovr_ranking[team]

    playoff_teams.sort(key=eff_rank_fn)
    seeds = { t:(i+1) for i,t in enumerate(playoff_teams)}
    
    return PlayoffMetadata(conf_champs=conf_champs, seeds=bidict(seeds))


sim_school_id_map = {}

with open("sportsref_to_sim_id.json", "r", encoding="utf-8") as ff:
    sim_school_id_map = json.load(ff)

sref_from_if_map = {}

for k in sim_school_id_map:
    sref_from_if_map[sim_school_id_map[k]] = k

t_year = 2024

seeds = get_playoff_seeds(t_year)

#print(seeds)

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
        break

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

    last_round = n_round


print(last_round)

