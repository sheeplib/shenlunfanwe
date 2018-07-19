# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 09:55:34 2018

@author: sheeplib
"""

import scrapy
# from lxml import etree
from shenlunfanwe.items import ShenlunfanweItem

class ShenlunfanweSpider(scrapy.Spider):
    name = "shenlunfanwe"
    allowed_domains = ["www.offcn.com"]
    start_urls = ["http://www.offcn.com/gjgwy/ziliao/164/"]

    def start_requests(self):
        first_page_url = 'http://www.offcn.com/gjgwy/ziliao/164/'
        yield scrapy.Request(url = first_page_url, callback = self.parsemenu)
    def parsemenu(self, response):
        nextpage = response.xpath(r'//div[@class="zg_main"]/div[@class="zg_mainbox_let fl"]/div[@class="zg_page list_pagebox"]/p/a[7]/@href').extract()[0]
#        print(nextpage) ## Tracing

        nextpage = response.urljoin(nextpage)
        
        if nextpage != response.url:
            yield scrapy.Request(url = nextpage, callback = self.parsemenu)
        
        articles = response.xpath(r'//div[@class="zg_main"]/div[@class="zg_mainbox_let fl"]/ul[@class="list"]/li/a/@href').extract()
        for article in articles:
            yield scrapy.Request(url = article, callback = self.parsearticle)
            print(article)
    def parsearticle(self, response):
        item = ShenlunfanweItem()
        position = response.xpath(r'//div[@class="zg_main"]/div[@class="zg_left"]')
        item['title'] = position.xpath(r'h1[@class="zg_show_tit"]/text()').extract()[0]
        print(item['title'])
        date = position.xpath(r'div[@class="zg_show_form"]/text()').extract()[0]
        item['date'] = date.replace('|','').strip()
        word = position.xpath(r'div[@class="zg_show_word"]/p/text()').extract() # list每个元素为一段落
        item['word'] = '\t'+'\n\t'.join(word)
        yield item