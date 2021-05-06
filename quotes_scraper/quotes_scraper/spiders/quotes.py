# -*- coding: utf-8 -*-
import scrapy
import os

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com/']
    start_urls = ['http://quotes.toscrape.com/page/1/']
    page = 0
    max_pages = 5

    #def __init__(self):

    def start_requests(self):
        file = self.settings["FEED_URI"]
        if os.path.isfile(file):
            with open(file, 'w') as f:
                f.truncate()
                print("'{0}' truncated ...".format(file))
        for url in self.start_urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def save_page(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def parse(self, response): # Scrapy’s default callback method
        self.page = self.page + 1
        if self.page > self.max_pages:
            print ("\n*** Maximum pages reached ({0}). Scraping stopped. ***\n".format(self.max_pages))
            return
        print("\n***************************\nparsing page {0}\n***************************\n".format(self.page))
        for quote in response.css('div.quote'):
            yield {
                'author': quote.css('small.author::text').extract_first()
                , 'text': quote.css('span.text::text').re(r'\“(.+)\”')[0]
                , 'tags': quote.css('div.tags a.tag::text').extract()
                , 'page_number': self.page
            }

        next_page = response.css('li.next a::attr(href)').extract_first()

        #if next_page is not None:
        #    next_page = response.urljoin(next_page)
        #    yield scrapy.Request(next_page, callback = self.parse, dont_filter = True)

        # same (shortcut!)
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse, dont_filter = True)
