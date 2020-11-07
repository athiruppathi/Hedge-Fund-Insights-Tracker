import scrapy


class AqrFeaturedSpider(scrapy.Spider):
    name = 'aqr_featured'
    allowed_domains = ['https://www.aqr.com/Insights#featured']
    start_urls = ['http://https://www.aqr.com/Insights#featured/']

    def parse(self, response):
        pass
