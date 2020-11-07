import scrapy


class KkrSpider(scrapy.Spider):
    name = 'kkr'
    allowed_domains = ['https://www.kkr.com/global-perspectives/publications']
    start_urls = ['http://https://www.kkr.com/global-perspectives/publications/']

    def parse(self, response):
        pass
