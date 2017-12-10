# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    #房屋编码
    housecode = scrapy.Field()
    #房屋简介
    housename = scrapy.Field()
    #小区
    houseregion = scrapy.Field()
    #房屋信息
    houseinfo = scrapy.Field()
    #面积
    housearea = scrapy.Field()
    #片区
    houseposition = scrapy.Field()
    #关注数
    houseattention = scrapy.Field()
    #带看数
    housefollow = scrapy.Field()
    #总价
    totalprice = scrapy.Field()
    #均价
    unitprice = scrapy.Field()
