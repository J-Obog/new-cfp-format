from bs4 import BeautifulSoup

def get_soup_from_file(filename: str) -> BeautifulSoup:
    with open(filename, "r") as f:
        return BeautifulSoup(f.read(), 'html.parser')
    
def get_soup_from_html(html_str: str) -> BeautifulSoup:
     return BeautifulSoup(html_str, 'html.parser')