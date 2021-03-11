import scrapy
from ..items import FundInsightsTrackerItem
from urllib.parse import urljoin
import re

class WilliamblairSpider(scrapy.Spider):
    name = 'williamblair'
    start_urls = ['https://active.williamblair.com/insights/blog/']

    def parse(self, response):
        items = FundInsightsTrackerItem()

        # Rest of articles
        entry = response.css('.et_pb_module_inner')
        titles = entry.xpath('.//*[@class="blogtopblock"]/a/text()').extract()   
        links = entry.xpath('.//*[@class="blogtopblock"]/a/@href').extract()
        dates = entry.xpath('.//*[@class="publisheddate"]/text()').extract() 

        # Data Cleaning
        titlesFinal = []
        for i in titles:
            if i not in titlesFinal:
                titlesFinal.append(i)
        linksFinal = []
        for i in links:
            if i not in linksFinal:
                linksFinal.append(i)
        datesFinal = []
        for i in dates:
            if i not in datesFinal:
                datesFinal.append(i)

        # Combine data into tuples
        williamblair_item = []
        for i in range(len(titlesFinal)):
            tupTitle = titlesFinal[i]
            tupLink = linksFinal[i]
            tupDate = datesFinal[i]
            tup = (tupTitle, tupLink, tupDate)
            williamblair_item.append(tup)

        items['williamblair_item'] = williamblair_item

        yield items


