import scrapy
from urllib.parse import urljoin
from ..items import FundInsightsTrackerItem
import re 

class BlackrockSpider(scrapy.Spider):
    name = 'blackrock'
    start_urls = ['https://www.blackrock.com/us/individual/insights']

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

        # Dates Data Cleaning
        dates = entry.xpath('.//*[@class="attribution-text"]/span[1]/text()')
        dates_list = dates[:6].extract()
        
        # Titles Data Cleaning
        pattern_newline = re.compile("\n")
        titles_list_new = []
        for i in titles_list:
            re.sub(pattern_newline,'',i)
            i = i.strip()
            titles_list_new.append(i)

        # Combine data into tuples
        blackrock_item = []
        for i in range(len(titles_list_new)):
            tupTitle = titles_list_new[i]
            tupLink = absolute_url_list[i]
            tupDate = dates_list[i]
            tup = (tupTitle, tupLink, tupDate)
            blackrock_item.append(tup)

        items['blackrock_item'] = blackrock_item
        
        yield items