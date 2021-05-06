# -*- coding: utf-8 -*-

import scrapy
import os
from mn_schools.items import DistrictItem, SchoolItem, ContactItem
import re


class DistrictsSpider(scrapy.Spider):

    name = 'districts'
    allowed_domains = ['https://www.greatschools.org']
    start_urls = ['https://www.greatschools.org/schools/districts/Minnesota/MN/']


    def print_total(self, message, total):
        print("\n")
        print("-----------------------------------------------------------------------")
        print("{:,} {}".format(total, message))
        print("-----------------------------------------------------------------------")
        print("\n")


    def start_requests(self):

        file = self.settings["FEED_URI"]

        if os.path.isfile(file):
            with open(file, 'w') as f:
                f.truncate()
                print("'{0}' truncated ...".format(file))

        for url in self.start_urls:
            yield scrapy.Request(url = url, callback = self.parse)


    def parse(self, response):

        dists = response.xpath('//div[@class="districts-cities-list"]//tr')

        fixed_districts = [
            'Eden Prairie Public School District'
            , 'Edina Public School District'
            , 'Hastings Public School District'
            , 'Hopkins Public School District'
            , 'Lakeville Public School District'
            , 'Mahtomedi Public School District'
            , 'Minneapolis Public School Dist.'
            , 'Mounds View Public School District'
            , 'Prior Lake-Savage Area Schools'
            , 'Rosemount-Apple Valley-Eagan School District'
            , 'South Washington County School Dist'
            , 'St. Michael-Albertville School Dist'
            , 'Wayzata Public School District'
            , 'Westonka Public School District'
        ]

        row_cnt = 0

        for dist in dists:

            # first row is column header
            row_class = dist.xpath('@class').extract()[0] if len(dist.xpath('@class').extract()) > 0 else ""
            if(row_class == "table-top-row"):
                print("\n!!! row header found ... skipping !!!\n")
                continue

            row_cnt = row_cnt + 1

            # test
            #if(row_cnt > 20):break

            print("\nparsing district {0}\n".format(row_cnt))

            item = DistrictItem()

            item['name'] = dist.xpath('td[1]/a/text()').extract()[0].strip()
            item['url'] = dist.xpath('td[1]/a/@href').extract()[0]
            item['city'] = dist.xpath('td[2]/text()').extract()[0].strip()
            item['county'] = dist.xpath('td[3]/text()').extract()[0].strip()


            if item['name'] not in fixed_districts:
                row_cnt = row_cnt - 1
                continue

            if item['url'] is not None:
                url = response.urljoin(item['url']) + 'schools/?gradeLevels=e'
                yield scrapy.Request(url, self.parse_schools, dont_filter = True, meta = {'ditem': item})


        self.print_total("districts parsed", row_cnt)



    def parse_schools(self, response):

        ditem = response.meta['ditem']
        print("current district (p2) = " + ditem['name'])

        divs = response.xpath('//div[@class="ptm notranslate"]')

        row_cnt = 0

        for div in divs:

            row_cnt = row_cnt + 1

            # test
            #if(row_cnt > 10):break

            print("\nparsing school {0}\n".format(row_cnt))

            item = SchoolItem()

            item['name'] = div.xpath('div/a[@class="open-sans_sb mbs font-size-medium rs-schoolName"]/text()').extract()[0].strip()
            item['url'] = div.xpath('div/a[@class="open-sans_sb mbs font-size-medium rs-schoolName"]/@href').extract()[0]
            item['address'] = div.xpath('div[@class="hidden-xs font-size-small rs-schoolAddress"]/text()').extract()[0].strip()

            if item['url'] is not None:
                url = response.urljoin(item['url']) + '#Neighborhood'
                yield scrapy.Request(url, self.parse_contact, dont_filter = True, meta = {'ditem': ditem, 'sitem': item})

        self.print_total("schools parsed", row_cnt)


    def parse_contact(self, response):

        ditem = response.meta['ditem']
        sitem = response.meta['sitem']

        div = response.xpath('//div[@class="neighborhood-module"]')

        item = ContactItem()

        item['principal_name'] = "".join(div.xpath('//div[@class="dib"]//span/text()').extract()) if len(div.xpath('//div[@class="dib"]//span/text()').extract()) > 0 else ""

        item['email'] = ""
        item['phone'] = ""
        hrefs = div.xpath('//div[@class="contact-row"]//a/@href').extract()
        for href in hrefs:
            if href.startswith("mailto:"):
                item['email'] = href.split(":")[1]
            if href.startswith("tel:"):
                item['phone'] = href.split(":")[1]

        item['website'] = div.xpath('//a[@target="_blank" and text()="Website"]/@href').extract()[0] if len(div.xpath('//a[@target="_blank" and text()="Website"]/@href').extract()) > 0 else ""

        yield {
            'district_name' : ditem['name']
            , 'district_url' : ditem['url']
            , 'district_city' : ditem['city']
            , 'district_county' : ditem['county']
            , 'school_name' : sitem['name']
            , 'school_url' : sitem['url']
            , 'school_address' : sitem['address']
            , 'principal_name' : item['principal_name']
            , 'principal_email': item['email']
            , 'school_phone' : item['phone']
            , 'school_website': item['website']
        }
