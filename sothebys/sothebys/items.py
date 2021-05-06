# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ContactItem(scrapy.Item):
    name = scrapy.Field()
    company = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip = scrapy.Field()
    phone1 = scrapy.Field()
    phone2 = scrapy.Field()
    image_link = scrapy.Field()

