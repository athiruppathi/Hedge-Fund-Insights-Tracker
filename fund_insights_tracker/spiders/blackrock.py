import scrapy
from urllib.parse import urljoin
from ..items import FundInsightsTrackerItem


class BlackrockSpider(scrapy.Spider):
    name = 'blackrock'
    start_urls = ['https://www.blackrock.com/us/individual/insights']

    custom_settings = {
        'FEED_FORMAT':'json',
        'FEED_URI':'blackrock_data.json'
    }

    def parse(self, response):

        items = FundInsightsTrackerItem()

        entry = response.css('ul.clearfix.row')
        titles = entry.xpath('.//*[@class="title"]/text()')
        titles_list = titles[:6].extract()

        links = entry.xpath('.//*[@class="read-article"]/a/@href')
        links2 = links[:6].extract()
        absolute_url_list = []
        for link in links2:
            absolute_url = response.follow(link, callback=self.parse)
            absolute_url_list.append(absolute_url)

        dates = entry.xpath('.//*[@class="attribution-text"]/span[1]/text()')
        dates_list = dates[:6].extract()

        items['blackrock_titles'] = titles_list
        items['blackrock_links'] = absolute_url_list
        items['blackrock_dates'] = dates_list
        
        yield items