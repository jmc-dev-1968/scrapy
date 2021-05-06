# -*- coding: utf-8 -*-

import scrapy
import os
from swift_codes.items import CountryItem, BankItem, BranchItem
import re
import logging
from datetime import datetime

class BanksSpider(scrapy.Spider):

    name = 'banks'
    allowed_domains = ['transferwise.com']
    start_urls = ['http://transferwise.com/gb/swift-codes/countries/']

    #configure_logging(install_root_handler=False)

    #logging.basicConfig(
    #    filename = 'log.txt',
    #    format = '%(levelname)s: %(message)s',
    #    level = logging.WARNING
    #)

    excepion_file =  open("exceptions.txt", 'w')
    excepion_file.truncate()

    def write_exception (self, message):
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.excepion_file.writelines("{} {}\n".format(ts, message ))

    country_count = 0
    bank_count = 0
    branch_count = 0
    total_bank_count = 0
    total_branch_count = 0

    def start_requests(self):

        file = self.settings["FEED_URI"]

        if os.path.isfile(file):
            with open(file, 'w') as f:
                f.truncate()
                print("\n'{0}' truncated ...\n".format(file))

        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

        #self.logger.info("Finished Processing : COUNTRY COUNT = {}, BANK COUNT = {}, BRANCH COUNT = {})".format(
        #    self.country_count
        #    , self.total_bank_count
        #    , self.total_branch_count)
        #)


    def parse(self, response):

        table = response.xpath('//a[starts-with(@href,"/gb/swift-codes/countries/") and not(@class)]')

        for row in table:

            item = CountryItem()

            self.country_count = self.country_count + 1
            self.total_bank_count = self.total_bank_count  + self.bank_count
            self.total_branch_count = self.total_branch_count  + self.branch_count
            self.bank_count = 0
            self.branch_count = 0

            item['name'] = row.xpath('text()').extract()[0].strip()
            item['path'] = row.xpath('@href').extract()[0].strip()

            if item['path'] is not None:
                url = response.urljoin(item['path'])
                yield scrapy.Request(url, callback = self.parse_banks, meta = {'country_item': item, 'page': 1})

            ## test
            #if self.country_count == 5:
            #    break

            #self.logger.info("Country {} processed : BANK COUNT = {}, BRANCH COUNT = {} ({})".format(
            #    item['name']
            #    , self.bank_count
            #    , self.branch_count
            #    , item['path'])
            #)

    def parse_banks(self, response):

        country_item = response.meta['country_item']
        page = response.meta['page']

        xstr = '//a[starts-with(@href,"{0}/")]'.format(country_item['path'])
        table = response.xpath(xstr)

        ## no rows found
        if not table:
            return

        for row in table:

            self.bank_count = self.bank_count + 1

            item = BankItem()

            item['country'] = country_item['name']
            item['name'] = row.xpath('text()').extract()[0].strip()
            item['path'] = row.xpath('@href').extract()[0].strip() if row.xpath('@href').extract() else ""
            item['page'] = str(page)

            if item['path'] is not None:
                url = response.urljoin(item['path'])
                yield scrapy.Request(url, callback = self.parse_branches, meta = {'bank_item': item, 'page': 1})
            else:
                self.write_exception("bank {} has no url ({})".format(item['name'], country_item['path']))

        page = page + 1
        url = response.url.split('?')[0]   # strip query string
        url_next_page = "{}?page={}".format(url, str(page))
        yield scrapy.Request(url_next_page, callback = self.parse_banks, meta = {'country_item': country_item, 'page': page})


    def parse_branches(self, response):

        bank_item = response.meta['bank_item']
        page = response.meta['page']

        table = response.xpath('//li[@class="list-group-item" and div/a/@href]')

        ## no rows found
        if not table:
            return

        for row in table:

            self.branch_count = self.branch_count + 1

            item = BranchItem()

            ## bank info
            item['country'] = bank_item['country']

            item['bank_name'] = bank_item['name']
            item['bank_path'] = bank_item['path']
            item['bank_page'] = bank_item['page']

            ## branch info

            href = row.xpath('div/a/@href').extract()[0].strip() if row.xpath('div/a/@href').extract() else ""
            if not href:
                item['branch_path'] = ""
                item['swift_code'] = ""
            else:
                item['branch_path'] = response.urljoin(href)
                item['swift_code'] = re.match(r'/gb/swift-codes/(.+)', href).groups()[0] if re.match(r'/gb/swift-codes/(.+)', href) else ""

            item['branch_name'] = row.xpath('small/span[@class="d-block"]/text()').extract()[0].strip() if row.xpath('small/span[@class="d-block"]/text()') else ""

            if not item['swift_code']:
                self.write_exception("WARNING bank/branch {}/{} has no swift code ({})".format(item['bank_name'], item['branch_name'], item['bank_path']))

            if not item['branch_name']:
                self.write_exception("WARNING bank/swift {}/{} has no branch name ({})".format(item['bank_name'], item['swift_code'], item['bank_path']))

            item['branch_address'] = "".join(row.xpath('small/span[not(@class)]/text()').extract())

            item['branch_page'] = page

            yield item

        page = page + 1
        url = response.url.split('?')[0]   # strip query string
        url_next_page = "{}?page={}".format(url, str(page))
        yield scrapy.Request(url_next_page, callback = self.parse_branches, meta = {'bank_item': bank_item, 'page': page})
