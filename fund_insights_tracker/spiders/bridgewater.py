import scrapy
from urllib.parse import urljoin
from ..items import FundInsightsTrackerItem

class BridgewaterSpider(scrapy.Spider):
    name = 'bridgewater'
    start_urls = ['https://www.bridgewater.com/research-and-insights']

    def parse(self, response):

        items = FundInsightsTrackerItem()


        entry = response.css('.PromoC-text')
        titles = entry.xpath('.//*[@class="PromoC-title"]/a/text()')
        titles_list = titles[:10].extract()

        links = entry.xpath('.//*[@class="PromoC-title"]/a/@href')
        links_list = links[:10].extract()
        
        #dates = entry.xpath('.//*[@class="PromoC-date"]/text()')
        #dates_list = dates[:10].extract()

        dates = []
        for i in range(len(titles_list)):
            dates.append('---')


        bridgewater_item = []
        for i in range(len(titles_list)):
            tupTitle = titles_list[i]
            tupLink = links_list[i]
            tupDate = dates[i]
            tup = (tupTitle, tupLink, tupDate)
            bridgewater_item.append(tup)

        items['bridgewater_item'] = bridgewater_item

        yield items