import scrapy


class PimcoSpider(scrapy.Spider):
    name = 'pimco'
    allowed_domains = ['https://www.pimco.com/en-us/insights']
    start_urls = ['http://https://www.pimco.com/en-us/insights/']

    def parse(self, response):
        pass
