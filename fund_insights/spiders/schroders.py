import scrapy


class SchrodersSpider(scrapy.Spider):
    name = 'schroders'
    allowed_domains = ['https://www.schroders.com/en/insights/']
    start_urls = ['http://https://www.schroders.com/en/insights//']

    def parse(self, response):
        pass
