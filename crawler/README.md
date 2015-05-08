> Crawler

Code for crawl menosdias website

>> Requeriments

* [scrappy](http://scrapy.org/) python
 
    pip install scrapy

>> Usage

Inside of crawler directory. For crawling website and saving entrance in json 
format

    scrapy crawl menosdias -o items.json -t json

Debuging a page of the website

    scrapy parse --spider=menosdias -d 1 'URL'


