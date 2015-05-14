# -*- coding: utf-8 -*-
import scrapy
from crawler.items import PostItem
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http                        import Request
from bs4 import BeautifulSoup, Comment
from itertools import chain
import re

re_tag=re.compile('<.*>')
re_if=re.compile('\[ if.*\]')

class MenosdiasSpider(scrapy.Spider):
    name = "menosdias"
    depth_limit= 0 
    allowed_domains = ["menosdiasaqui.blogspot.mx"]
    start_urls = (
        'http://menosdiasaqui.blogspot.mx/',
    )



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
            body=info_post.xpath('*/div[@class="post-body entry-content"]').extract()
            body=[x for x in body if not x.startswith('[')]
            item['body']=[]
            for content in body:
                content=BeautifulSoup(content)
                comments = content.findAll(text=lambda text:isinstance(text, Comment))
                [comment.extract() for comment in comments]
                comments = content.findAll(text=lambda text:isinstance(text, Comment))
                [comment.extract() for comment in comments]
                text=content.text
                text=re_tag.sub("",text)
                text=re_if.sub("",text)
                item['body'].append(text)


            mark=info_post.xpath('*/div[@class="post-body entry-content"]//b/text()').extract()
            item['mark']=[x for x in [m.strip() for m in mark] if len(x) > 0]
            # Extrae info footer
            footer=info_post.xpath('*/div[@class="post-footer"]')
            item['nameAuthor']=footer.xpath('.//span[@itemprop="name"]/text()').extract()
            item['datePublished']=footer.xpath('.//abbr[@itemprop="datePublished"]/@title').extract()
            item['url']=footer.xpath('.//a[@title="permanent link" and @class="timestamp-link"]/@href').extract()

            links=sel.xpath('//a[@class="blog-pager-older-link"]/@href').extract()
            for link in links:
                yield Request(link,self.parse)
            yield item

    def strip_tags(self,html):
        soup = BeautifulSoup(html)
        text = soup.text.strip()
        
        return text
