# -*- coding: utf-8 -*-

import scrapy


class Quotes2Spider(scrapy.Spider):
    name = 'quotes2'

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'

        tag = getattr(self, 'tag', None)
        page = getattr(self, 'page', None)

        #for attr in dir():
        #    print("{} => {}".format(attr, getattr(self, attr, None)))

        if tag is not None:
            #url = url + 'tag/' + tag
            url = "{}tag/{}".format(url, tag)

        if page is not None:
            url = "{}page/{}".format(url, page)

        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first()
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)