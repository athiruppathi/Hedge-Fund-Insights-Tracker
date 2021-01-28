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

        # Combine data into tuples
        schroders_item = []
        for i in range(len(titles_list)):
            tupTitle = titles_list[i]
            tupLink = absolute_url_list[i]
            tupDate = dates_list[i]
            tup = (tupTitle, tupLink, tupDate)
            schroders_item.append(tup)

        items['schroders_item'] = schroders_item

        yield items