import scrapy
from ..items import FundInsightsTrackerItem
from urllib.parse import urljoin
import re

class WilliamblairSpider(scrapy.Spider):
    name = 'williamblair'
    start_urls = ['https://www.williamblair.com/Research-and-Insights/Insights/Equity-Research.aspx']

    def parse(self, response):
        items = FundInsightsTrackerItem()

        entry = response.xpath('//*[@class="content-area"]')
        titles = entry.xpath('.//div/a/text()').extract()
        links = entry.xpath('.//div/a/@href').extract()
        absolute_url_list = []
        for i in links:
            absolute_url = response.follow(i, callback=self.parse)
            absolute_url_list.append(absolute_url)

        dates = []
        for i in titles:
            splitDates = i.split('|')
            dates.append(splitDates)
        

        datesFinal = []
        for i in dates:
            finalDate = i[1]
            datesFinal.append(finalDate)

        # Combine data into tuples
        williamblair_item = []
        for i in range(len(titles)):
            tupTitle = titles[i]
            tupLink = absolute_url_list[i]
            tupDate = datesFinal[i]
            tup = (tupTitle, tupLink, tupDate)
            williamblair_item.append(tup)

        items['williamblair_item'] = williamblair_item

        yield items


