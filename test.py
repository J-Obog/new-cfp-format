from bs4 import BeautifulSoup


data = ""
with open("rankings/cfp_2026.xls", "r") as f:
    data = f.read()

soup = BeautifulSoup(data, 'html.parser')

ss = soup.find_all("tr")

print(ss[1].has_attr("data-row"))
