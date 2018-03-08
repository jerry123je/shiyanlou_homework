# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from douban_movie.items import MovieItem


class AwesomeMovieSpider(scrapy.Spider):
    name = 'awesome-movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/subject/3011091']

    rules = (
            Rule(),
            )
    def parse_movie_item(self, response):
        
        return item

    def parse_start_url(self,response):
        yield self.parse_movie_item(response)

    def parse_page(self, response):
        yield self.parse_movie_item(response)

