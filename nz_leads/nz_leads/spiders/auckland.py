# -*- coding: utf-8 -*-
import scrapy
import json
import os

class AucklandSpider(scrapy.Spider):
    name = 'auckland'
    allowed_domains = ['https://unidirectory.auckland.ac.nz']
    #start_urls = ['https://unidirectory.auckland.ac.nz/search#?search=*&page=1&rows=20&orderBy=relevance']
    # start_urls = ['https://unidirectory.auckland.ac.nz/people/moar?hostKey=search&page=1&rows=20&search=*&startAt=0']
    page = 1
    startAt = 0
    rowsPerPage = 20
    baseUrl = 'https://unidirectory.auckland.ac.nz/people/moar?hostKey=search&page={0}&rows={1}&search=*&startAt={2}'
    max_pages = 430
    start_urls = [baseUrl.format(page, rowsPerPage, startAt)]

    def start_requests(self):
        file = self.settings["FEED_URI"]
        if os.path.isfile(file):
            with open(file, 'w') as f:
                f.truncate()
                print("'{0}' truncated ...".format(file))
        for url in self.start_urls:
            yield scrapy.Request(url = url, callback = self.parse_json)

    def get_json_attribute(self, json, attribute):
        if attribute in json and json[attribute] is not None:
            return json[attribute]
        else:
            return None

    def parse_json(self, response):

        if self.page > self.max_pages:
            print ("\n*** Maximum pages reached ({0}). Scraping stopped. ***\n".format(self.max_pages))
            return

        print("\nparsing page {0}\n".format(self.page))

        jresponse = json.loads(response.body_as_unicode())

        for profile in jresponse['profiles']:
            yield{
                'name' : self.get_json_attribute(profile, 'fullName')
                , 'emails' : self.get_json_attribute(profile, 'emailAddresses')
                , 'phones': self.get_json_attribute(profile, 'phoneNumbers')
            }

        self.page = self.page + 1
        pageUrl = self.baseUrl.format(self.page, self.rowsPerPage, (self.page - 1) * 20)
        yield scrapy.Request(url = pageUrl, callback = self.parse_json, dont_filter = True)


    def parse(self, response): # Scrapy’s default callback method
        self.page = self.page + 1
        if self.page > self.max_pages:
            print ("\n*** Maximum pages reached ({0}). Scraping stopped. ***\n".format(self.max_pages))
            return
        print("\n***************************\nparsing page {0}\n***************************\n".format(self.page))
        for quote in response.css('div.quote'):
            yield {
                'page_num': self.page
                , 'text': quote.css('span.text::text').re(r'\“(.+)\”')[0]
                , 'author': quote.css('small.author::text').extract_first()
                , 'tags': quote.css('div.tags a.tag::text').extract()
            }

        next_page = response.css('li.next a::attr(href)').extract_first()

        #if next_page is not None:
        #    next_page = response.urljoin(next_page)
        #    yield scrapy.Request(next_page, callback = self.parse, dont_filter = True)

        # same (shortcut!)
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse, dont_filter = True)

