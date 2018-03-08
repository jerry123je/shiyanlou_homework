# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from flask_doc.items import PageItem
import re


class FlaskSpider(scrapy.spiders.CrawlSpider):
    name = 'flask'
    allowed_domains = ['flask.pocoo.org']
    start_urls = ['http://flask.pocoo.org/docs/0.12/']

    rules = (
            Rule(LinkExtractor(restrict_xpaths=('//li[@class="toctree-l1"]/a')),callback=parse_page, follow=True),
            )

    def parse_page(self, response):
        item = PageItem()
        print(type(item))
        item['url'] = response.url
        item['text'] = response.css('div.body').extract_first()
        yield item
