import scrapy
from ..items import FundInsightsTrackerItem
import re 


class KkrSpider(scrapy.Spider):
    name = 'kkr'
    start_urls = ['https://www.kkr.com/global-perspectives/publications']



    def parse(self, response):
        items = FundInsightsTrackerItem()

        entry = response.css('.col-xs-12.col-sm-12.col-md-8.col-lg-8.__ot_dotline-v')
        titles = entry.xpath('.//h2/a/text()').extract()
        links = entry.xpath('.//h2/a/@href').extract()

        date_first = entry.xpath('.//*[@class="__mediaPost_list first-post"]/span/strong/text()').extract()
        #dates_entries = entry.xpath('.//*[@class="__mediaPost_list "]/*[@class="time"]/text()').extract()
        dates_entries = entry.xpath('.//div/div[2]/span/text()').extract()

        # Dates Data Cleaning
        firstList = []
        firstPattern = re.compile('• ')
        for i in date_first:
            i = re.split(firstPattern,i)
            firstList.append(i)
        
        secondList = []
        secondPattern = re.compile('[^A-Za-z0-9 ]+')
        for i in dates_entries:
            i = re.sub(secondPattern,'',i)
            i = i.strip()
            secondList.append(i)
        
        firstEntry = firstList[0][1]

        secondListNew = []
        for i in secondList:
            if len(i) > 2:
                secondListNew.append(i)
        secondListNew.insert(0,firstEntry)
        #dates_list = firstListNew + secondListNew
        
        items['kkr_titles'] = titles
        items['kkr_links'] = links
        items['kkr_dates'] = secondListNew

        yield items