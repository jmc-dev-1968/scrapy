# -*- coding: utf-8 -*-

import scrapy
import os, sys
from ca_salary.items import CityItem, CityYearItem
import re
from scrapy.http import Request


class Salary2Spider(scrapy.Spider):

    name = 'salary2'
    allowed_domains = ['transparentcalifornia.com']
    start_urls = ['https://transparentcalifornia.com/agencies/salaries/']

    def start_requests(self):

        # purge csv files
        file_count = 0
        dirs = os.listdir(self.settings["FILES_STORE"] + '/full') # wtf? why does scrapy created "full" subdir?
        for file in dirs:
            file_count = file_count + 1
            os.remove(self.settings["FILES_STORE"] + '/full/' + file)
        if file_count > 0 : self.logger.info('%s CSV files deleted', file_count)

        file = self.settings["FEED_URI"]

        if os.path.isfile(file):
            with open(file, 'w') as f:
                f.truncate()
                print("'{0}' truncated ...".format(file))

        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)


    def parse(self, response):

        city_count = 0

        cities = response.xpath('//table[@class="table table-condensed table-striped agency-list"]')[4]

        for city in cities.xpath('tbody//tr'):

            city_count = city_count + 1

            item = CityItem()

            item['link'] = city.xpath('td[1]/a/@href').extract()[0].strip()
            item['name'] = city.xpath('td[1]/a/text()').extract()[0].strip()
            item['code'] = item['link'].split("/")[3]

            #print("\n{0} ==> {1} ==> {2}".format(item['name'], item['link'], item['code']))

            if item['link'] is not None:
                url = response.urljoin(item['link'])
                yield scrapy.Request(url, self.parse_city, dont_filter = True, meta = {'city_item': item})

            #if city_count == 3:
            #    break

    def parse_city(self, response):

        city_item = response.meta['city_item']

        salary_years = response.xpath('//div[@id="view-downloads"]//p')

        for salary_year in salary_years:

            item = CityYearItem()

            item['city_name'] = city_item['name']
            item['description'] = salary_year.xpath('a/text()').extract()[0].strip()
            item['year'] = re.match(r'^.+?(\d{4})$', item['description']).group(1)

            csv_url = salary_year.xpath('a/@href').extract()[0].strip()

            item['file_urls'] = [csv_url]
            #item['files'] = [csv_url.split('/')[-1]]

            #yield{
            #  'city_name' : city_item['name']
            #  , 'city_code' : city_item['code']
            #  , 'city_link' : city_item['link']
            #  , 'salary_year_desc' : item['description']
            #  , 'salary_year' : item['year']
            #  , 'csv_file_link': item['link']
            #}

            yield item

            #yield Request(item['link'], self.save_csv)

            #print("  {0} ==> {1}".format(item['year'], item['link']))
