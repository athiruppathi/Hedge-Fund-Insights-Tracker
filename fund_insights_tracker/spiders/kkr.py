import scrapy
from ..items import FundInsightsTrackerItem


class KkrSpider(scrapy.Spider):
    name = 'kkr'
    start_urls = ['https://www.kkr.com/global-perspectives/publications']



    def parse(self, response):
        entry = response.css('.col-xs-12.col-sm-12.col-md-8.col-lg-8.__ot_dotline-v')
        titles = entry.xpath('.//h2/a/text()').extract()
        links = entry.xpath('.//h2/a/@href').extract()
        date = entry.xpath('.//*[@class="time"]/text()').extract()

        for i in date:
            i = i.strip()
