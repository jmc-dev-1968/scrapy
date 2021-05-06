# -*- coding: utf-8 -*-
import scrapy
import os
from nz_leads.items import WaikatoLeadItem


class WaikatoSpider(scrapy.Spider):
    name = 'waikato'
    allowed_domains = ['http://phonebook.waikato.ac.nz']
    start_urls = ['http://phonebook.waikato.ac.nz/cgi-bin/bluesearch/']

    def start_requests(self):
        file = self.settings["FEED_URI"]
        if os.path.isfile(file):
            with open(file, 'w') as f:
                f.truncate()
                print("'{0}' truncated ...".format(file))
        for url in self.start_urls:
            form_data = {"sname" : "*", "surname-anchor" : "+anywhere", "gname" : "", "extn" : "", "user" : "", "room" : "", "dept" : "", "submit" : "Search"}
            yield scrapy.FormRequest(url, callback = self.parse, formdata = form_data)

    def get_phone_from_ext(self, extension):
        if len(extension) == 0:
            return ""
        first_digit = extension[0]
        prefix = ""
        if first_digit == '4':
            prefix = "+64 7 838"
        elif first_digit == '5':
            prefix = "+64 7 858"
        elif first_digit == '9':
            prefix = "+64 7 837"
        elif first_digit == '8':
            prefix = "+64 7 557"

        return "{} {}".format(prefix, extension) if prefix != "" else  ""


    def get_list_item(self, list, index):
        if len(list) > 0:
            return list[index]
        else:
            return ""

    def parse(self, response):
        rows = response.xpath('//tr[@class="row0" or @class="row1"]')
        row_cnt = 0
        good_row_cnt  =0
        for row in rows:
            row_cnt = row_cnt + 1
            print("\nparsing row {0}\n".format(row_cnt))

            item = WaikatoLeadItem()

            item['name'] = row.xpath('td[@class="namecol"]/text()').extract()[0]
            item['extension'] = row.xpath('td[@class="phonecol"]/text()').extract()[0]
            item['username'] = self.get_list_item(row.xpath('td[@class="usercol"]/text()').extract(), 0)
            item['room'] = self.get_list_item(row.xpath('td[@class="roomcol"]/text()').extract(), 0)
            item['department'] = self.get_list_item(row.xpath('td[@class="deptcol"]/a/text()').extract(), 0)
            item['email'] = "{}@waikato.ac.nz".format(item['username'])
            item['phone'] =  self.get_phone_from_ext(item['extension'])

            if item['name'] != "" and item['email'] != "" and item['phone'] != "":
                good_row_cnt = good_row_cnt + 1
                yield item

        print("\n--------------------------------------------\ntotal/good rows parsed {:,}/{:,}\n--------------------------------------------\n".format(row_cnt, good_row_cnt))
