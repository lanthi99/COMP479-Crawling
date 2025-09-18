from pathlib import Path

import scrapy


class LinksSpider(scrapy.Spider):
    name = "linkspider"
    # start_urls = [
    #     "https://crawler-test.com/"
    # ]
    # allowed_domains = ["crawler-test.com", "quotes.toscrape.com", "example.com"]

    def __init__(self, start_url=None, allowed=None, upperBound=None, *args, **kwargs):
        super(LinksSpider, self).__init__(*args, **kwargs)
        if start_url:
            self.start_urls = start_url.split(',')
        if allowed:
            self.allowed_domains = allowed.split(',')
        if upperBound:
            self.limit = int(upperBound)
        self.count = 0


    def parse(self, response):
        if self.count >= self.limit:
            #close spider 
            self.crawler.engine.close_spider(self, 'limit reached')
            return
        
        self.count += 1
        yield { "url": response.url }

        for href in response.css("a::attr(href)").getall():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)
        

# benjamin.lofofollo@concordia.ca
# github repo link or python file