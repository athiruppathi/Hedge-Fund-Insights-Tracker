import scrapy


class BlackrockSpider(scrapy.Spider):
    name = 'blackrock'
    start_urls = ['https://www.blackrock.com/us/individual/insights']

    def parse(self, response):
        pass
