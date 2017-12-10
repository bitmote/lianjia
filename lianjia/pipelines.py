# -*- coding: utf-8 -*-
import sqlite3
import scrapy
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LianjiaPipeline(object):
    def __init__(self):
        #创建数据库
        self.conn = sqlite3.connect('lianjia.db')
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute("CREATE TABLE bjhouses(housecode text  not null,housename text not null,houseregion\
             text not null,houseinfo text,housearea float,houseposition text,houseattion int,housefollow int,houseprice float,unitprice float)")
        except sqlite3.Error, why:
            print why[0]

    def process_item(self, item, spider):
        #插入房屋信息
        ins = "insert into bjhouses values(?,?,?,?,?,?,?,?,?,?)"
        v = (item['housecode'],item['housename'],item['houseregion'],item['houseinfo'],item['housearea'],item['houseposition'],item['houseattention'],item['housefollow'],item['totalprice'],item['unitprice'])
        self.cursor.execute(ins,v)
        return item
    def close_spider(self,spider):
        self.conn.commit()
        self.conn.close()
