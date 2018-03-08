# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import redis
import json


class FlaskDocPipeline(object):
    def process_item(self, item, spider):
        item['text'] = re.sub(r'\n{2,}','\n',re.sub(r'<[^>]+>|[ ]{2,}','',item['text']))
        item = json.dumps(item.__dict__)
        self.redis.lpush('flask_doc:items',item)
        return item

    def open_spider(self, spider):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def close_spider(self, spider):
        self.redis.close()
