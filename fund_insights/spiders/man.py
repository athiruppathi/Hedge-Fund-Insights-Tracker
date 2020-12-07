import scrapy


class ManSpider(scrapy.Spider):
    name = 'man'
    allowed_domains = ['https://www.man.com/maninstitute/']
    start_urls = ['http://https://www.man.com/maninstitute//']

    def parse(self, response):
        pass
