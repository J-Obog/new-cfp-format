from bs4 import BeautifulSoup


data = ""
with open("rankings/cfp_2024.xls", "r") as f:
    data = f.read()

soup = BeautifulSoup(data, 'html.parser')

for row in soup.find_all("tr"):
    if row.has_attr("data-row"):
        rank = row.find("td", attrs={"data-stat": "rank"})["csk"].split(".")[0]
        col = row.find("td", attrs={"data-stat": "school_name"})["csk"].split(".")[0]
        poll_date = row.find("td", attrs={"data-stat": "date_poll"}).text
        
        if poll_date == "Final":
            print(poll_date, rank, col)
        #print()