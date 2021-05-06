# -*- coding: utf-8 -*-

import scrapy
import os
from ca_salary.items import SalaryItem
import re


class SalarySpider(scrapy.Spider):

    name = 'salary'
    allowed_domains = ['transparentcalifornia.com']
    start_urls = ['https://transparentcalifornia.com/salaries/2011/']

    page_count = 0

    def start_requests(self):

        file = self.settings["FEED_URI"]

        if os.path.isfile(file):
            with open(file, 'w') as f:
                f.truncate()
                print("'{0}' truncated ...".format(file))

        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    @staticmethod
    def strip_money(value):

        if value == "Not provided":
            return ""

        value = value.replace("$", "")
        value = value.replace(",", "")
        return value

    def parse(self, response):

        self.page_count = self.page_count + 1

        print("\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Processing Page {0}  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n".format(self.page_count))

        table = response.xpath('//table[@id="main-listing"]')

        for row in table.xpath('tbody//tr'):

            item = SalaryItem()

            item['name'] = row.xpath('td[1]/a/text()').extract()[0].strip()
            item['title'] = row.xpath('td[2]/a/text()').extract()[0].strip()

            item['employer'] = row.xpath('td[2]/small/a/text()').extract()[0].strip()
            item['year'] = ""

            match = re.match(r'^(.+?)(\d{4})$', item['employer'])
            if match:
                item['employer'] = match.group(1).strip().rstrip(",")
                item['year'] = match.group(2)

            item['regular'] = SalarySpider.strip_money(row.xpath('td[3]/text()').extract()[0].strip())
            item['overtime'] = SalarySpider.strip_money(row.xpath('td[4]/text()').extract()[0].strip())
            item['other'] = SalarySpider.strip_money(row.xpath('td[5]/text()').extract()[0].strip())

            item['total_pay'] = SalarySpider.strip_money(row.xpath('td[6]/text()').extract()[0].strip())
            item['total_benefits'] = SalarySpider.strip_money(row.xpath('td[7]/text()').extract()[0].strip())
            item['total'] = SalarySpider.strip_money(row.xpath('td[8]/text()').extract()[0].strip())

            yield item

        next_page = response.css('li.next a::attr(href)').extract_first()

        #if self.page_count >= 5:
        #    exit()

        if next_page is not None:
            yield response.follow(next_page, self.parse)



