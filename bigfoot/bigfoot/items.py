# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BigfootItem(scrapy.Item):

    name = scrapy.Field()
    description = scrapy.Field()

class RegionItem(scrapy.Item):

    name = scrapy.Field()
    type = scrapy.Field()
    country = scrapy.Field()
    url = scrapy.Field()
    listing_count = scrapy.Field()
