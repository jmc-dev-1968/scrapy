
from requests import get
from bs4 import BeautifulSoup

import urllib.request


#url = 'http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1'
#response = get(url)
#html_soup = BeautifulSoup(response.text, 'html.parser')
#movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')


url = "https://www.alims.gov.rs/eng/medicinal-products/search-for-human-medicines/?id=373900"

#response = urllib.request.urlopen(url)
#soup = BeautifulSoup(response, 'html.parser')

response = get(url)

soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('div', id = "sadrzaj").find("table")
print(table)

for tr in table.find_all('tr'):
    key_val = tr.find_all('td')
    print("{} => {}".format(key_val[0].get_text(), key_val[1].get_text()))
