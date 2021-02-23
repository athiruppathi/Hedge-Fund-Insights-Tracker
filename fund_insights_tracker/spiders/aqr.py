import scrapy
from urllib.parse import urljoin
from ..items import FundInsightsTrackerItem
import re 

class AqrSpider(scrapy.Spider):
    name = 'aqr'
    start_urls = ['https://www.aqr.com/Insights#learningcenter']

    def parse(self, response):
        items = FundInsightsTrackerItem()

        entry = response.css('div.insights-all-insights__articles')
        titles = entry.xpath('.//h4/a/text()').extract()
        dates = entry.xpath('.//h5/text()').extract()
        links = entry.xpath('.//h4/a/@href').extract()

        absolute_url_list = []
        for i in links:
            absolute_url = response.follow(i, callback=self.parse)
            absolute_url_list.append(absolute_url)

        print(absolute_url_list)
        aqr_item = absolute_url_list
        items['aqr_item'] = aqr_item
        yield items

        # Dates Cleaning
        dates_list = []
        for index, element in enumerate(dates):
            if index % 2 == 0:
                dates_list.append(element)
        
        dates_list_final = []
        for i in dates_list:
            for j in i:
                if j.isupper():
                    dateTitle = i.index(j)
            finalDate = i[dateTitle:]
            dates_list_final.append(finalDate)

        aqr_item = []
        for i in range(len(titles)):
            tupTitle = titles[i]
            tupLink = absolute_url_list[i]
            tupDate = dates_list_final[i]
            tup = (tupTitle, tupLink, tupDate)
            aqr_item.append(tup)

        items['aqr_item'] = aqr_item

        yield items  
