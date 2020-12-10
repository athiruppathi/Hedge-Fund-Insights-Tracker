import scrapy
from ..items import FundInsightsTrackerItem
from urllib.parse import urljoin

class WilliamblairSpider(scrapy.Spider):
    name = 'williamblair'
    start_urls = ['https://www.williamblair.com/Research-and-Insights/Insights/Equity-Research.aspx']

    custom_settings = {
        'FEED_FORMAT':'json',
        'FEED_URI':'williamblair.json'
    }

    def parse(self, response):
        items = FundInsightsTrackerItem()

        entry = response.xpath('//*[@class="content-area"]')
        titles = entry.xpath('.//div/a/text()').extract()
        links = entry.xpath('.//div/a/@href').extract()
        absolute_url_list = []
        for i in links:
            absolute_url = response.follow(i, callback=self.parse)
            absolute_url_list.append(absolute_url)
        
        items['williamblair_titles'] = titles
        items['williamblair_links'] = absolute_url_list

        yield items


