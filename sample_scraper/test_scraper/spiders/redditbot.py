# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import os

class RedditbotSpider(scrapy.Spider):

    name = 'redditbot'
    allowed_domains = ['https://www.reddit.com/r/thewalkingdead/']
    start_urls = ['https://www.reddit.com/r/thewalkingdead/']

    def parse(self, response):

        # truncate csv
        #print("Saved to : " + self.settings["FEED_URI"])
        csv_file = self.settings["FEED_URI"]
        if os.path.isfile(csv_file):
            with open(csv_file, 'w') as f:
                f.truncate()

        # Extracting the content using css selectors
        titles = response.css('.title.may-blank::text').extract()
        votes = response.css('.score.unvoted::text').extract()
        times = response.css('time::attr(title)').extract()
        times_utc = response.css('time::attr(datetime)').extract()
        comments = response.css('.comments::text').extract()

        # Give the extracted content row wise
        for item in zip(titles, votes, times, times_utc, comments):
            # create a dictionary to store the scraped info
            scraped_info = {
                'title': item[0]
                , 'vote': item[1]
                , 'created_at_str': item[2]
                , 'created_at': self.stringToDate(item[2])
                , 'created_at_utc': item[3]
                , 'comments': item[4]
            }

            # yield or give the scraped info to scrapy
            yield scraped_info

    def stringToDate(self, str_date):
        try:
            test_date = datetime.strptime(str_date, '%a %b %d %H:%M:%S %Y UTC')
            return test_date
        except ValueError as ex:
            return None
