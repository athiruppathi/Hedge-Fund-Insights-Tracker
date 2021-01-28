import scrapy
from urllib.parse import urljoin
from ..items import FundInsightsTrackerItem
import re

class PimcoSpider(scrapy.Spider):
    name = 'pimco'
    start_urls = ['https://www.pimco.com/en-us/insights']

    def parse(self, response):
        items = FundInsightsTrackerItem()

        entry = response.xpath('//article')
        titles = entry.xpath('.//*[@class="finderInsightTitle"]/text()').extract()
        links = entry.xpath('.//*[@class="finderInsightTitle"]/@href').extract()
        absolute_url_list = []
        for link in links:
            if len(link) > 50:
                links.remove(link)
            absolute_url = response.follow(link, callback=self.parse)
            absolute_url_list.append(absolute_url)


        dates = entry.xpath('.//time/text()').extract()
        datesFinal = dates[4:]

        # Titles Data Cleaning 
        titles_list = []
        for i in titles:
            if i not in titles_list:
                titles_list.append(i)

        # Combine data into tuples
        pimco_item = []
        for i in range(len(titles_list)):
            tupTitle = titles_list[i]
            tupLink = absolute_url_list[i]
            tupDate = datesFinal[i]
            tup = (tupTitle, tupLink, tupDate)
            pimco_item.append(tup)

        items['pimco_item'] = pimco_item
        
        yield items