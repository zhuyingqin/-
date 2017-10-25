# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class SinamicroblogItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class FansItem(Item):
    _id = Field()  # 用户ID
    fans = Field()  # 粉丝
