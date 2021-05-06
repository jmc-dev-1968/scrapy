# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CountryItem(scrapy.Item):

    name = scrapy.Field()
    path = scrapy.Field()


class BankItem(scrapy.Item):

    name = scrapy.Field()
    path = scrapy.Field()
    country  = scrapy.Field()
    page = scrapy.Field()

    #def __init__(self, country):
    #    self.country = country


class BranchItem(scrapy.Item):

    country  = scrapy.Field()

    bank_name = scrapy.Field()
    bank_path = scrapy.Field()
    bank_page = scrapy.Field()

    branch_name = scrapy.Field()
    branch_path = scrapy.Field()
    branch_page = scrapy.Field()
    branch_address = scrapy.Field()
    swift_code = scrapy.Field()


