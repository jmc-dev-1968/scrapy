# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpecialtyItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()

class DoctorItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()

class DoctorInfoItem(scrapy.Item):
    address = scrapy.Field()
    phone = scrapy.Field()
    fax = scrapy.Field()
    licenses = scrapy.Field()
    #license_period = scrapy.Field()
