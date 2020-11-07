import scrapy


class TwosigmaSpider(scrapy.Spider):
    name = 'twosigma'
    allowed_domains = ['https://www.twosigma.com/insights/']
    start_urls = ['http://https://www.twosigma.com/insights//']

    def parse(self, response):
        pass
