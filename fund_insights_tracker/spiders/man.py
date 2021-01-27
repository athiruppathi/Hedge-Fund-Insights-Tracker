import scrapy
from urllib.parse import urljoin
from ..items import FundInsightsTrackerItem
import re

class ManSpider(scrapy.Spider):
    name = 'man'
    start_urls = ['https://www.man.com/maninstitute/']
    custom_settings = {
        'FEED_FORMAT':'json',
        'FEED_URI':'man_data.json'
    }

    def parse(self, response):
        items = FundInsightsTrackerItem()

        entry = response.css('.col-12.col-md-6.col-lg-4.teaser__wrap.teaser__wrap--small')
        titles = entry.xpath('.//*[@class="teaser__content"]/h2/text()').extract()
        dates = entry.xpath('//*[@class="details__date"]/text()')
        dates_list = dates[2:14].extract()

        links = entry.xpath('.//a/@href').extract()
        absolute_url_list = []
        for link in links:
            absolute_url = response.follow(link, callback=self.parse)
            absolute_url_list.append(absolute_url)   

        # Titles Data Cleaning
        titlesFinal = []
        pattern = re.compile(': +$')
        for i in titles:                    # combine titles if one has colon and space in it 
            if bool(re.search(pattern, i)) == True:
            #if i.find(': ') == True:
                print('true')
                nextTitle = titles[titles.index(i) + 1]
                newTitle = i + nextTitle               
                titles.remove(i)
                #titles.remove(nextTitle)
                titlesFinal.append(newTitle)
            else:
                titlesFinal.append(i)

        # Combine data into tuples
        man_item = []
        for i in range(len(titlesFinal)):
            tupTitle = titlesFinal[i]
            tupLink = absolute_url_list[i]
            tupDate = dates_list[i]
            tup = (tupTitle, tupLink, tupDate)
            man_item.append(tup)

        items['man_item'] = man_item
        
        yield items