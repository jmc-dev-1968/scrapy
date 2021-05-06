# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MemberItem(scrapy.Item):

    type = scrapy.Field() # senator or representative
    name = scrapy.Field()
    region = scrapy.Field()
    positions = scrapy.Field()
    party = scrapy.Field()
    link = scrapy.Field()

    pass
