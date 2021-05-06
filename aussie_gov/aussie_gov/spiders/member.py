# -*- coding: utf-8 -*-

import scrapy
import os
from aussie_gov.items import MemberItem ## wtf? fix this!
import re
import logging
from datetime import datetime


class MemberSpider(scrapy.Spider):

    name = 'member'
    allowed_domains = ['www.aph.gov.au']
    start_urls = ['https://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results']

    def start_requests(self):
        file = self.settings["FEED_URI"]
        if os.path.isfile(file):
            with open(file, 'w') as f:
                f.truncate()
                print("'{0}' truncated ...".format(file))
        for url in self.start_urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):

        mems = response.xpath('//div[@class="medium-pull-2 medium-7 large-8  columns"]')

        mem_cnt = 0

        for mem in mems:

            mem_cnt = mem_cnt + 1

            item = MemberItem()

            print("\nparsing member {0}\n".format(mem_cnt))

            item['name'] = mem.xpath('h4[@class="title"]//a/text()').extract()[0] \
                if len(mem.xpath('h4[@class="title"]//a/text()').extract()) > 0 else ""

            if item['name'].startswith('Senator '):
                item['type'] = 'Senator'
                item['name'] = item['name'].replace('Senator ', '')
            else:
                item['type'] = 'Representative'

            item['link'] = mem.xpath('h4[@class="title"]//a/@href').extract()\
                if len(mem.xpath('h4[@class="title"]//a/@href').extract()) > 0 else ""

            item['region'] = mem.xpath('dl[@class="dl--inline__result text-small"]/dd[1]/text()').extract()[0]\
                if len(mem.xpath('dl[@class="dl--inline__result text-small"]/dd[1]/text()').extract()) > 0 else ""

            item['positions'] = ""
            item['party'] = ""

            yield item