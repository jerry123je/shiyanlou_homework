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
            item = ShiyanlougithubItem()
            item['name'] = repo.css('div.d-inline-block a::text').extract_first().strip()
            item['update_time'] = repo.css('div.f6 relative-time::attr(datetime)').extract_first()
            
            repo_url = response.urljoin(repo.css('div.d-inline-block a::attr(href)').extract_first())
            request = scrapy.Request(repo_url, callback=self.parse_repo)
            request.meta['item'] = item
            yield request


    def parse_repo(self,response):
        item = response.meta['item']
        number_summary = list(map(lambda x:x.strip(),response.css('ul.numbers-summary span::text').extract()))
        item['commits'] = number_summary[0]
        item['branches'] = number_summary[1]
        item['releases'] = number_summary[2]
        yield item

