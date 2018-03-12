# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import redis
import json
from scrapy.exceptions import DropItem

class DoubanMoviePipeline(object):
    movie_list = []
    def process_item(self, item, spider):
        #item['summary'] = re.sub('<[^>]+>','',str(item['summary']))
        item['name'] = str(item['name'])
        item['summary'] = str(item['summary'])
        item['score'] = float(item['score'])
        if item['score'] >= 8.0:
            if item['name'] not in self.movie_list:
                self.movie_list.append(item['name'])
                item = json.dumps(item.__dict__['_values'])
                self.redis.lpush("douban_movie:items",item)
            else:
                raise DropItem('Movie %s already logged'%item['name'])
        return item

    def open_spider(self, spider):
        self.redis = redis.StrictRedis(host="localhost", port=6379, db=0)

#    def close_spider(self, spider):
#        self.redis.close()
