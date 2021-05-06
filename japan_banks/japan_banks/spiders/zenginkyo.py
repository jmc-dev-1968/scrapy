# -*- coding: utf-8 -*-
import scrapy
import os
from japan_banks.items import JapanBanksItem
import re

class ZenginkyoSpider(scrapy.Spider):

    name = 'zenginkyo'
    allowed_domains = ['https://www.zenginkyo.or.jp']
    start_urls = ['https://www.zenginkyo.or.jp/en/outline/list-of-members/']

    def start_requests(self):
        file = self.settings["FEED_URI"]
        if os.path.isfile(file):
            with open(file, 'w') as f:
                f.truncate()
                print("'{0}' truncated ...".format(file))
        for url in self.start_urls:
            yield scrapy.Request(url = url, callback = self.parse)


    def parse(self, response):
        rows = response.xpath('//div[@class="body bodytext"]//li')
        row_cnt = 0
        good_row_cnt  =0
        for row in rows:
            row_cnt = row_cnt + 1
            print("\nparsing row {0}\n".format(row_cnt))

            item = JapanBanksItem()

            item['name'] = row.xpath('a/text()').extract()[0] if len(row.xpath('a/text()').extract()) > 0 else ""
            item['url'] = row.xpath('a/@href').extract()[0] if len(row.xpath('a/@href').extract()) > 0 else ""

            #match = re.match(r'^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$', item['url'])
            match = re.match(r'^((http[s]?|ftp):\/\/)?(www\.)?([^:\/\s]+)(.+?)$', item['url'])
            if match:
                _protocol = match.group(2)
                _www = match.group(3)
                _url = match.group(4)
                __remainder = match.group(5)
                item['base_url'] = _url
                item['protocol'] = _protocol

            if item['name'] != "" and item['url']:
                good_row_cnt = good_row_cnt + 1
                yield item

        print("\n--------------------------------------------\ntotal/good rows parsed {:,}/{:,}\n--------------------------------------------\n".format(row_cnt, good_row_cnt))
