import scrapy
from ..items import FundInsightsTrackerItem
from urllib.parse import urljoin

class CarillonSpider(scrapy.Spider):
    name = 'carillon'
    start_urls = ['https://www.carillontower.com/our-thinking']

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


        # Combine data into tuples
        carillon_item = []
        for i in range(len(titles)):
            tupTitle = titles[i]
            tupLink = absolute_url_list[i]
            tupDate = dates[i]
            tup = (tupTitle, tupLink, tupDate)
            carillon_item.append(tup)

        items['carillon_item'] = carillon_item

        yield items
