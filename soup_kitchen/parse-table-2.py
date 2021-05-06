
import urllib.request
from bs4 import BeautifulSoup

page = urllib.request.urlopen("https://www.alims.gov.rs/eng/medicinal-products/search-for-human-medicines/?id=373900")
html = page.read()

#soup = BeautifulSoup(html, features="lxml")
#table = soup.find("table", attrs={"class":"details"})

soup = BeautifulSoup(html, features="lxml") #.encode("utf-8")
div = soup.find("div", {"id":"sadrzaj"})

#print(div)
