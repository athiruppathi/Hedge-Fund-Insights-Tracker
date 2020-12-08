import scrapy
from urllib.parse import urljoin
from ..items import FundInsightsTrackerItem

class SchrodersSpider(scrapy.Spider):
    name = 'schroders'
    start_urls = ['https://www.schroders.com/en/insights/']

    def parse(self, response):
        items = FundInsightsTrackerItem()

        entry = response.css('.col-xs-12')
        titles = entry.xpath('.//h3/text()')
        titles_list = titles[1:].extract()

        dates = entry.xpath('.//*[@class="date"]/text()')
        dates_list = dates[1:].extract()

        links = entry.xpath('.//@href')
        absolute_url_list = []
        for link in links:
            absolute_url = response.follow(link, callback=self.parse)
            absolute_url_list.append(absolute_url)
        absolute_url_list = absolute_url_list[4:-11]
        
        items['schroders_titles'] = titles_list
        items['schroders_links'] = absolute_url_list
        items['schroders_dates'] = dates_list
        yield items
        
