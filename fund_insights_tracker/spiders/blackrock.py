import scrapy
from urllib.parse import urljoin
from ..items import FundInsightsTrackerItem


class BlackrockSpider(scrapy.Spider):
    name = 'blackrock'
    start_urls = ['https://www.blackrock.com/us/individual/insights']

    custom_settings = {
        'FEED_FORMAT':'csv',
        'FEED_URI':'blackrock_data.csv'
    }

    def parse(self, response):

        items = FundInsightsTrackerItem()

        entry = response.css('.read-article')
        titles = entry.xpath('//a/@title')
        titles2 = titles[8:14].extract()

        links = entry.xpath('//a/@href')
        links2 = links[8:14].extract()
        absolute_url_list = []
        for link in links2:
            absolute_url = response.follow(link, callback=self.parse)
            absolute_url_list.append(absolute_url)
        
        items['blackrock_titles'] = titles2
        items['blackrock_links'] = absolute_url_list
        
        yield items