#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

results = []

def parse(response):
    for comment in response.css('div.comment-list-item'):
        result = {}
        result['username'] = comment.css('div.user-username a::text').extract_first()
        result['username'] = result['username'].strip()
        result['content'] = comment.css('div.comment-item-content p').extract()
        result['content'] = re.sub('<[^>]+>','',' '.join(result['content']))
        results.append(result)
  
def has_next_page(response):    
    if not response.xpath('//li[@class="disabled next-page"]').extract():
        return True
    else:
        return False

def goto_next_page(driver):
    menu = driver.find_element_by_xpath('//div[@class="pagination-container"]')
    next_page = driver.find_element_by_xpath('//ul[@class="pagination"]/li[@class="next-page"]')
    ActionChains(driver).move_to_element(menu).click(next_page).perform()

def wait_page_return(driver, page):
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, '//ul[@class="pagination"]/li[@class="active"]'),
            str(page)
        )
    )

def spider():
    driver = webdriver.PhantomJS()
    url = 'https://www.shiyanlou.com/courses/427'
    driver.get(url)
    page = 1
    while True:
        wait_page_return(driver, page)
        html = driver.page_source
        response = HtmlResponse(url=url, body=html.encode('utf8'))
        parse(response)
        if not has_next_page(response):
            break
        page += 1
        goto_next_page(driver)
    #with open('/home/shiyanlou/comments.json', 'w') as f:
    with open('/tmp/comments.json', 'w') as f:
        f.write(json.dumps(results))

if __name__ == '__main__':
    spider()
