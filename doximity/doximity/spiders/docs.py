
import scrapy
import os
from doximity.items import DoctorItem, SpecialtyItem, DoctorInfoItem
import re
import random

class DocsSpider(scrapy.Spider):

    name = 'docs'
    allowed_domains = ['www.doximity.com']
    start_urls = ['https://www.doximity.com/directory/physicians/']

    spec_count = 0
    doc_count = 0

    #def load_user_agents(self):
    #    text_file = open("./doximity/spiders/user_agents.txt", "r")
    #    self.user_agents = text_file.readlines()

    #def get_random_user_agent(self):
    #    return random.choice(self.user_agents)

    def start_requests(self):

        file = self.settings["FEED_URI"]

        if os.path.isfile(file):
            with open(file, 'w') as f:
                f.truncate()
                print("'{0}' truncated ...".format(file))

        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)


    def parse(self, response):


        print("\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Processing Spec {0}  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n".format(self.spec_count))

        specs = response.xpath('//a[starts-with(@href, "/directory/md/specialty/")]')

        for spec in specs:

            self.spec_count = self.spec_count + 1

            item = SpecialtyItem()

            item['name'] = spec.xpath('text()').extract()[0].strip() if len(spec.xpath('text()').extract()) > 0 else ""
            item['link'] = spec.xpath('@href').extract()[0].strip() if len(spec.xpath('@href').extract()) > 0 else ""

            #print("{} ==> {}".format(item['name'], item['link']))

            #match = re.match(r'^(.+?)(\d{4})$', item['employer'])
            #if match:
            #    item['employer'] = match.group(1).strip().rstrip(",")
            #    item['year'] = match.group(2)

            if item['link'] is not None:
                url = response.urljoin(item['link'])
                yield scrapy.Request(url, self.parse_specialty, dont_filter = True, meta = {'sitem': item})

            #next_page = response.css('li.next a::attr(href)').extract_first()

            if self.spec_count >= 5:
                break

            #if next_page is not None:
            #    yield response.follow(next_page, self.parse)


    def parse_specialty(self, response):

        self.doc_count = 0

        sitem = response.meta['sitem']

        docs = response.xpath('//a[starts-with(@title, "View") and starts-with(@href, "/cv/")]')

        for doc in docs:

            self.doc_count = self.doc_count + 1

            item = DoctorItem()

            item['name'] = doc.xpath('text()').extract()[0].strip()
            item['link'] = doc.xpath('@href').extract()[0].strip()

            print("  {} ==> {}".format(item['name'], item['link']))

            if item['link'] is not None:
                url = response.urljoin(item['link'])
                #ua = self.get_random_user_agent()
                yield scrapy.Request(url, self.parse_doc_info, dont_filter = True,  meta = {'sitem': sitem, 'ditem': item})
                #yield scrapy.Request(url, self.parse_doc_info, dont_filter = True, headers = {"User-Agent": ua}, meta = {'sitem': sitem, 'ditem': item})

            if self.doc_count >= 100:
                break


    def parse_doc_info(self, response):

        sitem = response.meta['sitem']
        ditem = response.meta['ditem']

        info = response.xpath('//ul[boolean(@data-sel-address)]')

        item = DoctorInfoItem()

        item['address'] = "|".join(info.xpath('li/div[1]//text()').extract()) if len(info.xpath('li/div[1]//text()')) > 0 else ""
        item['phone'] = info.xpath('//span[@itemprop="telephone"]/text()').extract()[0] if len(info.xpath('//span[@itemprop="telephone"]/text()')) > 0 else ""
        item['fax'] =  info.xpath('//span[@itemprop="faxNumber"]/text()').extract()[0] if len(info.xpath('//span[@itemprop="faxNumber"]/text()')) > 0 else ""

        certs = response.xpath('//section[@class="section certification-info"]')

        license_list = ""
        for cert in certs.xpath('ul/li//strong/text()'):
            match = re.match(r'^([A-Z]{2}) State Medical License$', cert.extract())
            if match:
                license_list = license_list +  match.group(1).strip() + ","

        item['licenses'] = license_list.rstrip(",")

        #print("    {} / {} / {} / [{}]".format(item['address'], item['phone'], item['fax'], item['licenses']))

        yield {
            'doctor' : ditem['name']
            , 'licenses' : item['licenses']
            , 'specialty': sitem['name']
            , 'address' : item['address']
            , 'phone' : item['phone']
        }
