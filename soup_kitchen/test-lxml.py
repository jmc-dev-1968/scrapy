
from lxml import html
import requests

url = "https://www.alims.gov.rs/eng/medicinal-products/search-for-human-medicines/?id=373900"

page = requests.get(url)
tree = html.fromstring(page.content)

print(type(tree))
rows = tree.xpath('//div[@id="sadrzaj"]/table//tr')
#rows = tree.xpath('/div[@id="sadrzaj"]/table//tr')
print(type(rows))

print(rows)

for row in rows:
    print(row)
    #key = rows.xpath('td[1]/text()')
    #val = rows.xpath('td[2]/text()')
    #print("{} => {}".format(key, val))





