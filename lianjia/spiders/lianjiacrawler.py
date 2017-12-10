# -*- coding: utf-8 -*-
import scrapy
from lianjia.items import LianjiaItem
import re
class LianjiacrawlerSpider(scrapy.Spider):
    name = 'lianjiacrawler'
    allowed_domains = ['lianjia.com']
    start_urls = []
    base_url = 'https://bj.lianjia.com/ershoufang/'
    #各区地址
    district = ['haidian', 'dongcheng', 'xicheng', 'fengtai', 'chaoyang', 'changping', 'daxing', 'yizhuangkaifaqu',
                'shijingshan', 'tongzhou', 'shunyi', 'fangshan', 'mentougou', 'pinggu', 'huairou']
    for item in district:
        url = base_url + item + '/pg1'
        if item in ['haidian', 'chaoyang']:
            #海淀朝阳房屋较多，分楼层来选择
            for height in ['lc1', 'lc2', 'lc3', 'lc4', 'lc5']:
                aurl = url + '{0}'.format(height)
                start_urls.append(aurl)
        else:
            start_urls.append(url)


#找出要爬取的信息，送入管道
#给出下一个要爬取的网页，提交sheduler
    #对于像朝阳这样的二手房数量多的区，需要按照底中高定楼层进行划分，但是对于像怀柔，密云等多数区，直接用网址就可以，
    #所以要在parse函数进行判断，如果是朝阳和海淀区，则按照楼层重新给出爬取的网址
    def parse(self, response):
        sel = scrapy.Selector(response)
        #总的页数
        total =eval(sel.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()[0])['totalPage']
        item = LianjiaItem()
        for index in range(1,total+1):
            str_index = str(index)
            #给出所有页面的网址
            url = re.sub(r'(\d+?)',str_index,response.url,1)
            yield scrapy.Request(url,callback = self.parse_item)

    def parse_item(self, response):
        sel = scrapy.Selector(response)
        item = LianjiaItem()
        houses = sel.xpath('//li[@class="clear"]')
        for house in houses:
            #这样写的问题是没有容错性，只能期望链家的数据比较规范
            housecode = house.xpath('./a/@data-housecode').extract()[0]
            housename = house.xpath('./div/div[@class="title"]/a/text()').extract()[0]
            houseregion = house.xpath('./div[1]/div[2]/div/a/text()').extract()[0]
            houseinfo = house.xpath('./div[1]/div[2]/div/text()').extract()[0]
            housearea = re.findall(ur'(\d+\.?\d*)平米',houseinfo)[0]
            houseposition = house.xpath('./div[1]/div[3]/div[1]/a/text()').extract()[0]
            followinfo = house.xpath('./div[1]/div[4]/text()').extract()[0]
            houseattention = re.findall(ur'(\d+)人关注',followinfo)[0]
            housefollow = re.findall(ur'(\d+)次带看',followinfo)[0]
            totalprice = house.xpath('./div[1]/div[6]/div[1]/span/text()').extract()[0]
            unitprice = house.xpath('./div[1]/div[6]/div[2]/@data-price').extract()[0]
            item['housecode'] = housecode
            item['housename'] = housename
            item['houseregion'] = houseregion.replace(' ','')
            print item['houseregion']
            item['houseinfo'] = houseinfo
            item['housearea'] = float(housearea)
            item['houseposition'] = houseposition
            item['houseattention'] = int(houseattention)
            item['housefollow'] = int(housefollow)
            item['totalprice'] = float(totalprice)
            item['unitprice'] = float(unitprice)

            yield item