import scrapy
from urllib.parse import urljoin
from ..items import FundInsightsTrackerItem
import re

class PimcoSpider(scrapy.Spider):
    name = 'pimco'
    start_urls = ['https://www.pimco.com/en-us/insights']
    custom_settings = {
        'FEED_FORMAT':'json',
        'FEED_URI':'pimco_data.json'
    }

    def parse(self, response):
        items = FundInsightsTrackerItem()

        entry = response.css('.article-wrapper.cf-article')
        titles = entry.xpath('.//*[@class="finderInsightTitle"]/text()').extract()
        links = entry.xpath('.//article/header/h1/a/@href').extract()
        absolute_url_list = []
        for link in links:
            absolute_url = response.follow(link, callback=self.parse)
            absolute_url_list.append(absolute_url)

        dates = entry.xpath('.//article/footer/div/time').extract()

        # Titles Data Cleaning 
        titles_list = []
        for i in titles:
            if i not in titles_list:
                titles_list.append(i)
        
        # Links Data Cleaning
        linksRemovalList = [absolute_url_list[0],absolute_url_list[2],absolute_url_list[4],absolute_url_list[6],absolute_url_list[8]]

        # Dates Data Cleaning
        datePattern1 = re.compile('<time>')
        datePattern2 = re.compile('</time>')

        dates_v1 = []
        for i in dates:
            i = re.sub(datePattern1,'',i)
            dates_v1.append(i)
        
        dates_v2 = []
        for j in dates_v1:
            j = re.sub(datePattern2,'',j)
            dates_v2.append(j)
    
        items['pimco_titles'] = titles_list
        items['pimco_links'] = linksRemovalList
        items['pimco_dates'] = dates_v2

        yield items