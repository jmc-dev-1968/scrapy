# -*- coding: utf-8 -*-

import scrapy
from bigfoot.items import RegionItem
import os
import re

class BfroSpider(scrapy.Spider):

    name = 'bfro'
    allowed_domains = ['www.bfro.net']
    start_urls = ['http://www.bfro.net/gdb/']

    exception_file = "exceptions.txt"

    def write_exception (self, message):
        f = open(self.exception_file, 'w')
        f.writelines("{}\n".format(message))
        f.close()

    @staticmethod
    def truncate_file(file):
        if os.path.isfile(file):
            with open(file, 'w') as f:
                f.truncate()
                print("\n'{0}' truncated ...\n".format(file))

    def start_requests(self):

        self.truncate_file(self.exception_file)
        self.truncate_file(self.settings["FEED_URI"])

        start_url =  self.start_urls[0]
        print("\nscraping page : {}\n".format(start_url))
        yield scrapy.Request(start_url, self.parse_states)


    def parse_states(self, response):

        xstr = '//table[@class="countytbl"]'
        tbls = response.xpath(xstr)

        if not tbls:
            return

        total_listing_count = 0

        for tbl in tbls:

            country = ""
            region_type = tbl.xpath('tr[1]/td[1]//text()').extract()[0]

            if region_type == "State":
                country = 'USA'
            elif region_type == "Province":
                country = 'Canada'
            else:
                continue

            name = ""
            url = ""
            listing_count = ""

            row_count = 0
            for row in tbl.xpath('.//tr'):

                row_count = row_count + 1

                ## first row is header ...
                if row_count == 1:
                    continue

                item = RegionItem()

                name = row.xpath('td[1]//text()').extract()[0].strip()
                url = row.xpath('td[1]/b/a/@href').extract()[0].strip() if row.xpath('td[1]/b/a/@href') else ""
                listing_count = row.xpath('td[2]//text()').extract()[0].strip()

                total_listing_count = total_listing_count + int(listing_count)

                item['name'] = name
                item['type'] = region_type
                item['country'] = country
                item['url'] = response.urljoin(url)
                item['listing_count'] = listing_count

                yield item

                #print("{} ({}) ==> {}".format(name, url, listing_count))


            print("\n-------------------------\n{} {}s Processed for {}\n-------------------------\n".format(str(row_count - 1), region_type, country))

        print("\n-------------------------\nTotal Listing Count = {}\n-------------------------\n".format(str(total_listing_count)))



                #item = StateItem()
            #item['description'] = row.xpath('text()').extract()[0].strip()
            #item['name'] = row.xpath('a/text()').extract()[0].strip()
            #item['path'] = row.xpath('a/@href').extract()[0].strip()
            #item['page'] = page
            #item['page_path'] = response.url


            #print("    {} ==> {}".format(item['name'], item['path']))

            #if not item['path']:
            #    self.write_exception("missing link : '{}' ({})".format(item['name'], response.url))
            #    continue

            #yield scrapy.Request(item['path'], self.parse_drug, meta={'page_item': item})
