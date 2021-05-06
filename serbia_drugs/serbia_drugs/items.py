# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DrugLiteItem(scrapy.Item):

    name = scrapy.Field()
    description = scrapy.Field()
    path = scrapy.Field()
    page = scrapy.Field()
    page_path = scrapy.Field()


class DrugItem(scrapy.Item):

    id = scrapy.Field()
    page = scrapy.Field()
    page_path = scrapy.Field()
    path = scrapy.Field()

    medicine_name = scrapy.Field()
    inn_common_name = scrapy.Field()
    types_of_solutions = scrapy.Field()
    classification = scrapy.Field()
    form_and_packing = scrapy.Field()
    ma_number = scrapy.Field()
    ma_date = scrapy.Field()
    expiration_date_solutions = scrapy.Field()
    manufacturer = scrapy.Field()
    mfc_address = scrapy.Field()
    mfc_country = scrapy.Field()
    marketing_authorisation_holder = scrapy.Field()
    mkt_address = scrapy.Field()
    atc_code = scrapy.Field()
    jkl = scrapy.Field()
    ean = scrapy.Field()
    type_of_medicine = scrapy.Field()
    summary_of_the_characteristics_of_the_medicine = scrapy.Field()
    instructions_to_the_patient = scrapy.Field()
    the_text_for_outer_and_inner_packaging = scrapy.Field()
    approved_changes = scrapy.Field()


class UrlItem(scrapy.Item):

    base_url = scrapy.Field()
    parm_signature = scrapy.Field()
    page = scrapy.Field()
