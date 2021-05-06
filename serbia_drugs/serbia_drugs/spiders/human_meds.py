# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import FormRequest
from serbia_drugs.items import DrugItem, UrlItem, DrugLiteItem
import os
import re
import logging
from datetime import datetime

class HumanMedsSpider(scrapy.Spider):

    name = 'human_meds'

    allowed_domains = ['www.alims.gov.rs']
    start_urls = ['https://www.alims.gov.rs/eng/medicinal-products/search-for-human-medicines/']

    #log_file = 'log.txt'
    #logging.basicConfig(filename = log_file)

    exception_file = "exceptions.txt"

    def write_exception (self, message):
        f = open(self.exception_file, 'w')
        f.writelines("{}\n".format(message))
        f.close()

    @staticmethod
    def truncate_file(file):
        if os.path.isfile(file):
            with open(file, 'w') as f:
                f.truncate()
                print("\n'{0}' truncated ...\n".format(file))


    def start_requests(self):

        self.truncate_file(self.exception_file)
        self.truncate_file(self.settings["FEED_URI"])
        #self.truncate_file(self.log_file)


        # initial request needs form data
        form_data = {
            "naziv_novi": "",
            "inn": "svi",
            "proizvodjac": "svi",
            "nosilac": "svi",
            "rezim": "svi",
            "atc": "svi",
            "jkl": "svi",
            "broj_resenja": "svi",
            "datum_resenja": "svi",
            "tip": "svi",
            "button": "Search",
            "MM_insert": "form1"
        }

        #url_item = UrlItem()
        #url_item['base_url'] =  self.start_urls[0]
        #url_item['parm_signature'] = 'pageNum_Recordset1={}&totalRows_Recordset1=6264&a=p&a=s'
        #url_item['page'] = 1
        #url = "{}?{}".format(url_item['base_url'], url_item['parm_signature'].format("1"))

        start_url =  "{}?a=p".format(self.start_urls[0])
        print("\nscraping page : {}\n".format(start_url))
        yield scrapy.FormRequest(start_url, self.parse, formdata = form_data,  meta = {'base_url': self.start_urls[0], 'page': 0})

        ## use proxy
        #request =  scrapy.FormRequest(start_url, self.parse, formdata = form_data,  meta = {'url_item': url_item})
        #request.meta['proxy'] = "localhost:8080"
        #yield request


    def parse(self, response):

        base_url = response.meta['base_url']
        page  = response.meta['page']

        xstr = '//div[@id="sadrzaj"]/ul//li'
        rows = response.xpath(xstr)

        if not rows:
            return

        for row in rows:

            item = DrugLiteItem()
            item['description'] = row.xpath('text()').extract()[0].strip()
            item['name'] = row.xpath('a/text()').extract()[0].strip()
            item['path'] = row.xpath('a/@href').extract()[0].strip()
            item['page'] = page
            item['page_path'] = response.url


            print("    {} ==> {}".format(item['name'], item['path']))

            if not item['path']:
                self.write_exception("missing link : '{}' ({})".format(item['name'], response.url))
                continue

            yield scrapy.Request(item['path'], self.parse_drug, meta={'page_item': item})

        #if page==5:
        #    return

        parm_sig = 'pageNum_Recordset1={}&totalRows_Recordset1=6264&a=p&a=s'
        page = page + 1
        next_url = "{}?{}".format(base_url, parm_sig.format(str(page)))
        print("\nscraping page : {}\n".format(next_url))
        yield scrapy.Request(next_url, self.parse,  meta = {'base_url': base_url, 'page': page})


    def parse_drug(self, response):

        item = DrugItem()

        item['page_path'] = response.meta['page_item']['page_path']
        item['page']  = response.meta['page_item']['page']
        item['path'] = response.url
        item['id'] = re.match(".+?id=(\d+)$", item['path']).groups()[0]

        xstr = '//div[@id="sadrzaj"]/table//tr'
        rows = response.xpath(xstr)

        if not rows:
            return

        is_first_address = True

        for row in rows:

            key = row.xpath('td[1]/strong/text()').extract()[0].strip() if row.xpath('td[1]/strong/text()') else ""
            if not key:
                continue

            val = row.xpath('td[2]/text()').extract()[0].strip() if row.xpath('td[2]/text()') else ""
            link = row.xpath('td[2]/a/@href').extract()[0].strip() if row.xpath('td[2]/a/@href') else ""

            # TODO find a way to pass a list of chars
            key = key.replace("/", "_")
            key = key.replace(" ", "_")
            key = key.replace(":", "")
            key = key.lower()

            if key == 'address' and  is_first_address:
                key = 'mfc_' + key
                is_first_address = False

            if key == 'country':
                key = 'mfc_' + key

            if key == 'address' and not is_first_address:
                key = 'mkt_' + key
                is_first_address = False

            pdf_fields = ['summary_of_the_characteristics_of_the_medicine', 'instructions_to_the_patient', 'the_text_for_outer_and_inner_packaging']
            if key in pdf_fields and not val:
                val = link

            item[key] = val

        yield item
