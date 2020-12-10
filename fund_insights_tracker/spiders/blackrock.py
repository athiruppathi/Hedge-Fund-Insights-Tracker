import scrapy
from urllib.parse import urljoin
from ..items import FundInsightsTrackerItem
import re 

class BlackrockSpider(scrapy.Spider):
    name = 'blackrock'
    start_urls = ['https://www.blackrock.com/us/individual/insights']
    custom_settings = {
        'FEED_FORMAT':'json',
        'FEED_URI':'blackrock_data.json'
    }

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

        dates = entry.xpath('.//*[@class="attribution-text"]/span[1]/text()')
        dates_list = dates[:6].extract()
        
        # Titles Data Cleaning
        pattern_newline = re.compile("\n")
        titles_list_new = []
        for i in titles_list:
            re.sub(pattern_newline,'',i)
            i = i.strip()
            titles_list_new.append(i)

        items['blackrock_titles'] = titles_list_new
        items['blackrock_links'] = links_list_new
        items['blackrock_dates'] = dates_list
        
        yield items