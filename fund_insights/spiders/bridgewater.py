import scrapy


class BridgewaterSpider(scrapy.Spider):
    name = 'bridgewater'
    start_urls = ['https://www.bridgewater.com/research-and-insights']

    def parse(self, response):
        pass
