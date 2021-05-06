# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class NzLeadsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class OtagoLeadItem(scrapy.Item):
    name = scrapy.Field()
    position = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()

class WaikatoLeadItem(scrapy.Item):
    name = scrapy.Field()
    extension = scrapy.Field()
    username = scrapy.Field()
    department = scrapy.Field()
    room = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
