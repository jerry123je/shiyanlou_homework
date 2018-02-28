# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from shiyanlougithub.models import Repositories, engine
from shiyanlougithub.items import ShiyanlougithubItem
from scrapy.exceptions import DropItem


class ShiyanlougithubPipeline(object):
    def process_item(self, item, spider):
        item['name'] = str(item['name'])
        item['update_time'] = datetime.strptime(item['update_time'].split('T')[0], '%Y-%m-%d')
        self.session.add(Repositories(**item))
        return item

    def open_spider(self,spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self,spider):
        self.session.commit()
        self.session.close()
