# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import ShiyanlougithubItem


class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'
    
    @property
    def start_urls(self):
        url_tmp = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmp.format(i) for i in range(1,5))

    def parse(self, response):
        for repo in response.css('li.col-12'):
            yield ShiyanlougithubItem({
                'name': repo.css('div.d-inline-block a::text').extract_first().strip(),
                'update_time': repo.css('div.f6 relative-time::attr(datetime)').extract_first()
                })
