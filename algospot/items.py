# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AlgospotItem(scrapy.Item):
    uid = scrapy.Field()
    name = scrapy.Field()
    submitted = scrapy.Field()
    accepted = scrapy.Field()
    source = scrapy.Field()
    category = scrapy.Field()

