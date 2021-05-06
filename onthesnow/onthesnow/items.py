# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SnowItem(scrapy.Item):
    season = scrapy.Field()
    resort = scrapy.Field()
    site = scrapy.Field()
    date = scrapy.Field()
    metric = scrapy.Field() # fall / depth
    value = scrapy.Field()
