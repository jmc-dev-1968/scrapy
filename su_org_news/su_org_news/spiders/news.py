# -*- coding: utf-8 -*-

import scrapy
import os
from su_org_news.items import NewsItem
#import re


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['https://su.org']
    #start_urls = [
    #    'https://su.org/about/press-room/news/'
    #    , 'https://su.org/su-faculty-news/'
    #    , 'https://su.org/su-community-news/'
    #]

    #start_urls = ['https://su.org/about/press-room/news/']
    #start_urls = ['https://su.org/su-faculty-news/']
    start_urls = ['https://su.org/su-community-news/']


    def print_total(self, message, total):
        print("\n")
        print("-----------------------------------------------------------------------")
        print("{:,} {}".format(total, message))
        print("-----------------------------------------------------------------------")
        print("\n")


    def start_requests(self):

        file = self.settings["FEED_URI"]

        if os.path.isfile(file):
            with open(file, 'w') as f:
                f.truncate()
                print("'{0}' truncated ...".format(file))

        for url in self.start_urls:
            yield scrapy.Request(url = url, callback = self.parse)


    def parse(self, response):


        articles = response.xpath('//div[@class="item-listing col-xs-12"]')
        #articles = response.xpath('//div[@class="item-listing col-xs-12"]//div[@class="content"]/h3/text()').extract()

        row_cnt = 0

        for article in articles:

            row_cnt = row_cnt + 1

            # test
            #if(row_cnt > 20):break

            #print("\nparsing article {0}\n".format(row_cnt))

            item = NewsItem()


            item['title'] = article.xpath('div[@class="content"]/h3/text()').extract()[0].strip()

            if len(article.xpath('div[@class="content"]/p[@class="date"]/text()').extract()) > 0:
                item['date'] = article.xpath('div[@class="content"]/p[@class="date"]/text()').extract()[0].strip()
                item['summary'] = "".join(article.xpath('div[@class="content"]/p[2]//text()').extract())
            else:
                item['date'] = ""
                item['summary'] = "".join(article.xpath('div[@class="content"]/p[1]//text()').extract())

            item['link'] = article.xpath('div[@class="cta"]/a/@href').extract()[0].strip()

            #print("{}\n{}\n{}\n{}\n\n".format(item['title'], item['date'], item['link'], item['summary']))

            yield item


        self.print_total("articles parsed", row_cnt)
