
import scrapy
import re
import os

class AuthorSpider(scrapy.Spider):
    name = 'authors'
    start_urls = ['http://quotes.toscrape.com/']
    auth_cnt = 0

    def print_bold(self, text):
        print("\n{div}\n{text}\n{div}\n".format(text = text, div = "*" * 50))

    def start_requests(self):

        # TODO is there a more compact way to return the already-interpolated value of FEED_URI?
        file = self.settings["FEED_URI"] % {'name' : self.name} #name parmeter substituion
        if os.path.isfile(file):
            with open(file, 'w') as f:
                f.truncate()
                self.print_bold("file '{}' truncated!".format(file))
        for url in self.start_urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):

        ## follow links to author pages (css method)
        # css
        #for href in response.css('.author + a::attr(href)'):
        ## follow links to author pages (xpath method)
        for href in response.xpath('//span/small[@class="author"]/following-sibling::a/@href'):
            yield response.follow(href, self.parse_author)

        # follow pagination links
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)


    def parse_author(self, response):

        self.auth_cnt = self.auth_cnt + 1

        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        def re_single_match(text, re_pattern):
            match = re.match(re_pattern, text)
            return match.group(1) if match else ""

        yield {
            'name': extract_with_css('h3.author-title::text')
            , 'birth_date': extract_with_css('.author-born-date::text')
            # can't use re with extract_with_css as it returns a list, have to use reponse object directlty
            #, 'birth_place': response.css('.author-born-location::text').re(r'in (.+)')[0].strip()
            , 'birth_place': re_single_match(extract_with_css('.author-born-location::text'), r'in (.+)')
        }

    def closed(self, reason):
        self.print_bold("{} authors parsed".format(self.auth_cnt))

