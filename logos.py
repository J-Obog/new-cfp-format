import time
from sportsref import SportsrefUtil 
import os
import requests

BASE_LOGO_URI = "https://cdn.ssref.net/req/202510241/tlogo/ncaa"

SPECIAL_MAPPINGS = {
    "Bowling Green": "bowling-green-state", 
    "BYU": "brigham-young",
    "Louisiana": "louisiana-lafayette",
    "LSU": "louisiana-state", 
    "Miami (FL)": "miami-fl", 
    "Miami (OH)": "miami-oh",
    "Middle Tennessee State": "middle-tennessee-state",
    "Ole Miss": "mississippi",
    "Pitt": "pittsburgh", 
    "Sam Houston": "sam-houston-state",
    "SMU": "southern-methodist", 
    "Texas A&M": "texas-am", 
    "UAB": "alabama-birmingham", 
    "UCF": "central-florida",
    "USC": "southern-california",
    "UTEP": "texas-el-paso", 
    "UTSA": "texas-san-antonio"
}

sportsref_cfb_schools = SportsrefUtil.get_sportsref_active_schools()

for school in sportsref_cfb_schools:
    logo_filepath = f"files/sportsref/team_logos/{school}.png"

    if os.path.exists(logo_filepath):
        continue
    
    normalized_name = SPECIAL_MAPPINGS[school] if school in SPECIAL_MAPPINGS else '-'.join(school.lower().split(' '))

    res = requests.get(f"{BASE_LOGO_URI}/{normalized_name}-2025.png")

    if res.status_code != 200:
        print(f"Something went wrong while processing {school}")
        continue

    with open(logo_filepath, "wb+") as outfile:
        outfile.write(res.content)

    time.sleep(1)