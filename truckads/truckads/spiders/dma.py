# -*- coding: utf-8 -*-

import scrapy
from truckads.items import MarketItem, DmaItem
import os
import logging
from datetime import datetime
import re

class DmaSpider(scrapy.Spider):

    name = 'dma'
    allowed_domains = ['www.truckads.com']
    start_urls = ['http://www.truckads.com/designated-market-map.asp']

    logging.basicConfig(filename = 'log.txt')

    excepion_file =  open("exceptions.txt", 'w')
    excepion_file.truncate()

    def write_exception (self, message):
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #self.excepion_file.writelines("{} {}\n".format(ts, message ))
        self.excepion_file.writelines("{}\n".format(message ))

    @staticmethod
    def truncate_file(file):
        if os.path.isfile(file):
            with open(file, 'w') as f:
                f.truncate()
                print("\n'{0}' truncated ...\n".format(file))

    def start_requests(self):

        output_file = self.settings["FEED_URI"]
        self.truncate_file(output_file)

        self.truncate_file("log.txt")

        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)


    def parse(self, response):

        xstr = '//form[@action="designated-market-map.asp"]//option[starts-with(@value,"https://www.truckads.com/Designated-Market/")]'
        table = response.xpath(xstr)

        #print("LEN => " + str(len(table.extract())))
        #return

        count = 0

        for row in table:

            count = count + 1

            item = MarketItem()

            item['name'] = row.xpath('text()').extract()[0].strip()
            item['path'] = row.xpath('@value').extract()[0].strip()

            self.write_exception("'{}' processing market ".format(item['name']))

            if item['path'] is not None:
                url = item['path']
                yield scrapy.Request(url, callback = self.parse_dma, meta = {'market_item': item})

            #if count == 3:
            #    return


    def parse_dma(self, response):

        market_item = response.meta['market_item']

        self.write_exception("'{}' processing zip codes ".format(market_item['name']))

        #xstr = '//p[contains(u/font/b/text(),"DESIGNATED MARKET ZIP CODES")]/font/text()'
        #zip_codes = response.xpath(xstr).extract()[0].strip().replace('\n', '').replace('\r', '').replace('\t', '').replace('"', '') if response.xpath(xstr).extract() else "*** ZIP CODES NOT FOUND ***"

        zip_codes = ""
        xstr = '//font[@size="1" and @face="Verdana" and @color="#666666"]/text()'
        for text in response.xpath(xstr).extract():

            clean_text = "".join(text).replace('\n','').replace('\r', '').replace('\t', '').replace(' ', '') + "," # trailing commas makes regex matching easier ...

            # corrector (for zip codes not comma separated)
            if re.match(r'\d{10}', clean_text):
                clean_text = re.sub('(\d{5})(\d{5})', r'\1,\2', clean_text)

            if re.match(r"^(\d{5},)+$", clean_text):
                zip_codes = re.match("^(.+),$", clean_text).groups()[0]

        #item = DmaItem()
        #item['market_name'] = market_item['name']
        #item['zip_code'] = zip_codes

        #yield item


        for zip_code in zip_codes.split(','):

            item = DmaItem()
            item['market_name'] = market_item['name']
            item['zip_code'] = zip_code

            yield item
