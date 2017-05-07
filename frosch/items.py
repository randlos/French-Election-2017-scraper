# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class com(scrapy.Item):
    commune = scrapy.Field()
    kandidat = scrapy.Field()
    stimmen = scrapy.Field()
    pass

class dep(scrapy.Item):
    departement = scrapy.Field()
    kandidat = scrapy.Field()
    stimmen = scrapy.Field()
    pass

