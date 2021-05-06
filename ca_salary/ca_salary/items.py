# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SalaryItem(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    employer = scrapy.Field()
    year = scrapy.Field()
    regular = scrapy.Field()
    overtime = scrapy.Field()
    other = scrapy.Field()
    total_pay = scrapy.Field()
    total_benefits = scrapy.Field()
    total = scrapy.Field()

class CityItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    code = scrapy.Field()

class CityYearItem(scrapy.Item):
    city_name = scrapy.Field()
    description = scrapy.Field()
    year = scrapy.Field()
    #link = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()