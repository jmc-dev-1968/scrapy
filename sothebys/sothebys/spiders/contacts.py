# -*- coding: utf-8 -*-

import scrapy
import os
from sothebys.items import ContactItem
#import re


class ContactsSpider(scrapy.Spider):

    name = 'contacts'
    allowed_domains = ['www.sothebysrealty.com']
    start_urls = [
        'https://www.sothebysrealty.com/eng/associates/wa-usa/40-pp'
    ]

    page_count = 0

    def start_requests(self):

        file = self.settings["FEED_URI"]

        if os.path.isfile(file):
            with open(file, 'w') as f:
                f.truncate()
                print("'{0}' truncated ...".format(file))

        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)


    def parse(self, response):

        self.page_count = self.page_count + 1

        print("\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Processing Page {0}  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n".format(self.page_count))

        contacts = response.xpath('//div[starts-with(@class, "default--1-2 lap--1-1 palm--1-1 palm-wide--1-1 grid__item has-ingrid-unspaced")]')

        for contact in contacts:

            item = ContactItem()

            item['image_link'] = contact.xpath('.//noscript/img/@src').extract()[0].strip()
            # contacts[0].xpath('.//noscript/img/@src').extract()[0]


            print("==> {}".format(item['image_link']))

            #match = re.match(r'^(.+?)(\d{4})$', item['employer'])
            #if match:
            #    item['employer'] = match.group(1).strip().rstrip(",")
            #    item['year'] = match.group(2)

            #yield item

        #next_page = response.css('li.next a::attr(href)').extract_first()

        #if self.page_count >= 5:
        #    break

        #if next_page is not None:
        #    yield response.follow(next_page, self.parse)
