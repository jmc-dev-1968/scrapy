# -*- coding: utf-8 -*-
import scrapy
from nz_leads.items import OtagoLeadItem
import os

#from html.parser import HTMLParser
from scrapy.selector import Selector

class OtagoSpider(scrapy.Spider):
    name = 'otago'
    allowed_domains = ['http://www.otago.ac.nz']
    start_urls = ['http://www.otago.ac.nz/contacts/search/index.html?query=%2B64']

    def start_requests(self):
        file = self.settings["FEED_URI"]
        if os.path.isfile(file):
            with open(file, 'w') as f:
                f.truncate()
                print("'{0}' truncated ...".format(file))
        for url in self.start_urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def get_list_item(self, list, index):
        if len(list) > 0:
            return list[index]
        else:
            return ""

    def parse(self, response):
        table = response.xpath('//div[@class="phonebook"]//table')
        row_cnt = 0
        rows = table.xpath('//tr')
        for row in rows:
            row_cnt = row_cnt + 1
            print("\nparsing row {0}\n".format(row_cnt))

            item = OtagoLeadItem()

            firstname = self.get_list_item(row.xpath('td[1]/text()[normalize-space(.)]').extract(), 0)
            lastname = "".join(row.xpath('td[1]/node()[not(self::span)]//text()[normalize-space(.)]').extract())
            position = "".join(row.xpath('td[1]/node()[self::span]//text()[normalize-space(.)]').extract())

            item['name']  = (firstname + ' ' + lastname).replace('\xa0', ' ').rstrip().lstrip()
            item['position']  = position
            item['phone'] = row.xpath('td[3]/a[starts-with(@href,"tel:")]/text()').extract()
            item['email'] = row.xpath('td[3]/a[starts-with(@href,"mailto:")]/text()').extract()

            yield item
