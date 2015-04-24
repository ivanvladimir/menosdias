# -*- coding: utf-8 -*-
import scrapy
from crawler.items import PostItem
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from bs4 import BeautifulSoup

class MenosdiasSpider(scrapy.Spider):
    name = "menosdias"
    allowed_domains = ["http://menosdiasaqui.blogspot.mx"]
    start_urls = (
        'http://www.http://menosdiasaqui.blogspot.mx/',
    )


    rules = [ 
        Rule(
            SgmlLinkExtractor(
                allow=[r'\d{4}/\d{2}/\w+']),
                callback='parse',follow=True)]

    def parse(self, response):
        for sel in response.xpath('//*[@class="date-outer"]'):
            item = PostItem()
            # Extrae título
            item['title']=sel.xpath('*[@class="date-header"]/span/text()').extract()
            # Extrae id info
            info_post=sel.xpath('*/div[@class="post-outer"]')
            item['blogId']=info_post.xpath('div/meta[@itemprop="blogId"]/@content').extract()
            item['postId']=info_post.xpath('div/meta[@itemprop="postId"]/@content').extract()
            # Extrae el cuerpo
            body=info_post.xpath('*/div[@class="post-body entry-content"]/div').extract()
            item['body']=[t for t in [self.strip_tags(div) for div in body] if len(t)>0]
            mark=info_post.xpath('*/div[@class="post-body entry-content"]//b/text()').extract()
            item['mark']=[x for x in [m.strip() for m in mark] if len(x) > 0]
            # Extrae info footer
            footer=info_post.xpath('*/div[@class="post-footer"]')
            item['nameAuthor']=footer.xpath('.//span[@itemprop="name"]/text()').extract()
            item['datePublished']=footer.xpath('.//abbr[@itemprop="datePublished"]/@title').extract()
            item['url']=footer.xpath('.//a[@title="permanent link"]/@href').extract()
            
            yield item

    def strip_tags(self,html):
        soup = BeautifulSoup(html)
        text = soup.text.strip()
        
        return text
