# -*- coding: utf-8 -*-

import scrapy
import os
from onthesnow.items import SnowItem
#import re

class SnowstatsSpider(scrapy.Spider):

    name = 'snowstats'
    allowed_domains = ['https://www.onthesnow.com']
    start_urls = ['https://www.onthesnow.com/colorado/breckenridge/historical-snowfall.html']

    sites = [
        'alberta/lake-louise',
        'alberta/marmot-basin',
        'alberta/ski-banff-norquay',
        'alberta/sunshine-village',
        'australia/falls-creek-alpine-resort',
        'australia/mt-buller',
        'australia/mt-hotham',
        'australia/perisher',
        'tyrol/kitzbuehel',
        'tyrol/mayrhofen',
        'salzburg/saalbach-hinterglemm-leogang',
        'tyrol/st-anton-am-arlberg',
        'salzburg/zell-am-see-schmittenhoehe',
        'british-columbia/big-white',
        'british-columbia/fernie-alpine',
        'british-columbia/kicking-horse',
        'british-columbia/panorama-mountain',
        'british-columbia/red-resort',
        'british-columbia/revelstoke-mountain',
        'british-columbia/silver-star',
        'british-columbia/sun-peaks',
        'british-columbia/whistler-blackcomb',
        'pirin/bansko',
        'rila/borovets',
        'california/bear-mountain',
        'california/bear-valley',
        'california/boreal',
        'california/ski-china-peak',
        'california/heavenly-mountain-resort',
        'california/homewood-mountain-resort',
        'california/kirkwood',
        'california/mammoth-mountain-ski-area',
        'california/mountain-high',
        'california/northstar-california',
        'california/snow-summit',
        'california/snow-valley',
        'california/soda-springs',
        'california/squaw-valley-usa',
        'california/sugar-bowl-resort',
        'california/tahoe-donner',
        'chile/el-colorado',
        'chile/la-parva',
        'chile/ski-portillo',
        'chile/valle-nevado',
        'colorado/arapahoe-basin-ski-area',
        'colorado/aspen-snowmass',
        'colorado/aspen-snowmass',
        'colorado/beaver-creek',
        'colorado/breckenridge',
        'colorado/aspen-snowmass',
        'colorado/copper-mountain-resort',
        'colorado/crested-butte-mountain-resort',
        'colorado/echo-mountain',
        'colorado/eldora-mountain-resort',
        'colorado/keystone',
        'colorado/loveland',
        'colorado/monarch-mountain',
        'colorado/powderhorn',
        'colorado/durango-mountain-resort',
        'colorado/aspen-snowmass',
        'colorado/steamboat',
        'colorado/telluride',
        'colorado/vail',
        'colorado/winter-park-resort',
        'colorado/wolf-creek-ski-area',
        'northern-alps/alpe-dhuez',
        'northern-alps/chamonix-mont-blanc',
        'northern-alps/courchevel',
        'northern-alps/la-plagne',
        'northern-alps/les-menuires',
        'northern-alps/megeve',
        'northern-alps/meribel',
        'northern-alps/morzine',
        'southern-alps/serre-chevalier',
        'northern-alps/tignes',
        'northern-alps/val-thorens',
        'idaho/bogus-basin',
        'idaho/lookout-pass-ski-area',
        'idaho/sun-valley',
        'illinois/chestnut-mountain-resort',
        'indiana/paoli-peaks',
        'aosta-valley/cervinia-breuil',
        'aosta-valley/courmayeur',
        'piemonte/sauze-doulx',
        'piemonte/sestriere',
        'maine/sugarloaf',
        'maine/sunday-river',
        'maryland/wisp',
        'massachusetts/jiminy-peak',
        'massachusetts/ski-butternut',
        'massachusetts/wachusett-mountain-ski-area',
        'michigan/boyne-highlands',
        'michigan/boyne-mountain-resort',
        'michigan/crystal-mountain',
        'michigan/timber-ridge',
        'montana/big-sky-resort',
        'montana/bridger-bowl',
        'montana/whitefish-mountain-resort',
        'new-hampshire/attitash',
        'new-hampshire/bretton-woods',
        'new-hampshire/cannon-mountain',
        'new-hampshire/loon-mountain',
        'new-hampshire/mount-sunapee',
        'new-hampshire/pats-peak',
        'new-hampshire/waterville-valley',
        'new-hampshire/wildcat-mountain',
        'new-jersey/mountain-creek-resort',
        'new-mexico/angel-fire-resort',
        'new-mexico/enchanted-forest-cross-countryski-area',
        'new-mexico/ski-apache',
        'new-mexico/taos-ski-valley',
        'new-york/belleayre',
        'new-york/gore-mountain',
        'new-york/greek-peak',
        'new-york/hunter-mountain',
        'new-york/peekn-peak',
        'new-york/whiteface-mountain-resort',
        'new-york/windham-mountain',
        'north-carolina/appalachian-ski-mtn',
        'north-carolina/cataloochee-ski-area',
        'north-carolina/sugar-mountain-resort',
        'ontario/blue-mountain',
        'ontario/horseshoe-resort',
        'oregon/mount-ashland',
        'oregon/mt-bachelor',
        'oregon/mt-hood-meadows',
        'oregon/mt-hood-ski-bowl',
        'pennsylvania/camelback-mountain-resort',
        'pennsylvania/elk-mountain-ski-resort',
        'pennsylvania/sno-mountain',
        'pennsylvania/seven-springs',
        'quebec/edelweiss-valley',
        'quebec/mont-sainte-anne',
        'quebec/mont-sutton',
        'quebec/tremblant',
        'quebec/ski-bromont',
        'quebec/stoneham',
        'new-zealand/cardrona-alpine-resort',
        'new-zealand/coronet-peak',
        'new-zealand/the-remarkables',
        'new-zealand/treble-cone',
        'valais/saas-fee',
        'graubunden/engadin-st-moritz',
        'valais/verbier',
        'valais/zermatt',
        'tennessee/ober-gatlinburg-ski-resort',
        'utah/alta-ski-area',
        'utah/brian-head-resort',
        'utah/brighton-resort',
        'utah/deer-valley-resort',
        'utah/park-city-mountain-resort',
        'utah/powder-mountain',
        'utah/snowbasin',
        'utah/snowbird',
        'utah/solitude-mountain-resort',
        'utah/sundance',
        'vermont/jay-peak',
        'vermont/killington-resort',
        'vermont/mad-river-glen',
        'vermont/mount-snow',
        'vermont/okemo-mountain-resort',
        'vermont/smugglers-notch-resort',
        'vermont/stowe-mountain-resort',
        'vermont/stratton-mountain',
        'vermont/sugarbush',
        'washington/crystal-mountain',
        'washington/mission-ridge',
        'washington/mt-baker',
        'washington/white-pass',
        'west-virginia/canaan-valley-resort',
        'west-virginia/snowshoe-mountain-resort',
        'west-virginia/winterplace-ski-resort',
        'wisconsin/cascade-mountain',
        'wisconsin/devils-head',
        'wyoming/grand-targhee-resort',
        'wyoming/jackson-hole',
        'wyoming/snow-king-resort'
    ]

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

        metric = "top" # snow / top
        years = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']

        site_cnt = 0
        for site in self.sites:
            site_cnt= site_cnt + 1
            base_url = "https://www.onthesnow.com/{0}/historical-snowfall.html".format(site)
            for year in years:
                url = "{0}?y={1}&q={2}".format(base_url, year, metric)
                yield scrapy.Request(url, self.parse, meta = {'metric': metric, 'year': year, 'site' : site})
            #if site_cnt > 1:
            #    exit()


    def parse(self, response):

        metric = response.meta['metric']
        year = response.meta['year']
        site = response.meta['site']
        season = "{0}/{1}".format(year, str(int(year) + 1))
        resort = response.xpath('//span[@class="resort_name"]/text()').extract()[0].strip()

        month_cals = response.xpath('//div[@class="cal_chart_div" or @class="cal_chart_div last"]')

        month_cnt = 0

        for month_cal in month_cals:

            month_cnt = month_cnt + 1

            print("\nparsing month {0}\n".format(month_cnt))

            item = SnowItem()

            month_year = month_cal.xpath('table/tr/th/strong[@class="dte_mon"]/text()').extract()[0].strip()

            item['season'] = season
            item['resort'] = resort
            item['site'] = site
            item['metric'] = metric

            #print("{}\n{}\n{}\n{}\n\n".format(item['season'], item['resort'], item['date'], item['metric']))

            days = month_cal.xpath('table[@class="cal_chart cal_chart_td"]/tr//td[@class="dte_hd_td"]')

            day_cnt = 0

            for day in days:

                day_cnt = day_cnt + 1

                the_day = day.xpath('span/text()').extract()[0].strip()
                item['value'] = day.xpath('div/text()').extract()[0].strip() if len(day.xpath('div/text()').extract()) > 0 else "0"

                #TODO : filter this out in the XPATH expression
                if not the_day.isnumeric():
                    continue
                else:
                    item['date'] = the_day + " " + month_year
                    yield item

            self.print_total("days parsed", day_cnt)

        self.print_total("months parsed", month_cnt)
