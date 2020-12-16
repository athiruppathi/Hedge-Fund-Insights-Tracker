import scrapy
from ..items import FundInsightsTrackerItem
from urllib.parse import urljoin

class CarillonSpider(scrapy.Spider):
    name = 'carillon'
    start_urls = ['https://www.carillontower.com/our-thinking']
    custom_settings = {
        'FEED_FORMAT':'json',
        'FEED_URI':'carillon_data.json'
    }

    def parse(self, response):
        items = FundInsightsTrackerItem()

        entry = response.xpath('//*[@class="col-xs-12 col-md-6"]')
        entry = entry[:19]

        titles = entry.xpath('.//h3/text()').extract()
        links = entry.xpath('.//*[@class="cl-btn-un"]/a/@href').extract()
        absolute_url_list = []
        for link in links:
            absolute_url = response.follow(link, callback=self.parse)
            absolute_url_list.append(absolute_url)

        dates = []
        for i in range(len(titles)):
            dates.append('---')
        
        items['carillon_titles'] = titles
        items['carillon_links'] = absolute_url_list
        items['carillon_dates'] = dates

        yield items
