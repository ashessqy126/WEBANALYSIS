# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
   title = scrapy.Field()
   link = scrapy.Field()
class MatchItem(scrapy.Item):
	degree = scrapy.Field()
	code = scrapy.Field()