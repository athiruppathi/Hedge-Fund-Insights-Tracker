import scrapy
from urllib.parse import urljoin
from ..items import FundInsightsTrackerItem

class BridgewaterSpider(scrapy.Spider):
    name = 'bridgewater'
    start_urls = ['https://www.bridgewater.com/research-and-insights']

    custom_settings = {
        'FEED_FORMAT':'json',
        'FEED_URI':'bridgewater_data.json'
    }

    def parse(self, response):

        items = FundInsightsTrackerItem()

        entry = response.css('.PromoC-title')
        titles = entry.xpath('.//a/text()')
        titles_new = titles[:10].extract()

        links = entry.xpath('.//a/@href')
        links_new = links[:10].extract()

        items['bridgewater_titles'] = titles_new
        items['bridgewater_links'] = links_new
        
        yield items