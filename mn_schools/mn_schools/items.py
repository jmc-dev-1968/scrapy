# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DistrictItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()

class SchoolItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    address = scrapy.Field()

class ContactItem(scrapy.Item):
    principal_name = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()

