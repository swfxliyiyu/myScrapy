# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ExchangeRateItem(scrapy.Item):
    # define the fields for your item here like:
    # 日期:
    date = scrapy.Field()
    # 美元:
    dollar = scrapy.Field()
    # 欧元
    euro = scrapy.Field()
    # 日元
    yen = scrapy.Field()
    # 港币
    hk = scrapy.Field()
    # 英镑
    pound = scrapy.Field()
    # 澳大利亚元
    australian = scrapy.Field()
    # 新西兰元
    new_zealand = scrapy.Field()
    # 新加坡元
    singapore = scrapy.Field()
    # 瑞士法郎
    swiss_franc = scrapy.Field()
    # 加拿大
    canada = scrapy.Field()
    # 林吉特
    myr = scrapy.Field()
    # 俄罗斯卢布
    rub = scrapy.Field()
    # 南非兰特
    zar = scrapy.Field()
    # 韩元
    south_korean = scrapy.Field()
    # 阿联酋迪拉姆
    rahm = scrapy.Field()
    # 沙特里亚尔
    sar = scrapy.Field()