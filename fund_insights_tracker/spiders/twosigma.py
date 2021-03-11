import scrapy
from ..items import FundInsightsTrackerItem
from scrapy.http import Request
import re 

class TwosigmaSpider(scrapy.Spider):
    name = 'twosigma'
    start_urls = ['https://www.twosigma.com/topic/markets-economy/']

    def parse(self, response):
        global links
        global titleList; global linksList; global datesList; global count
        count = 0
        titleList = []
        linksList = []
        datesList = []
        
        entry = response.xpath('//*[@class="postBlock"]')
        #titles = entry.xpath('.//h3/a/text()').extract()
        links = entry.xpath('.//h3/a/@href').extract()

        for link in links:
            yield Request(link, callback=self.parse_date, cb_kwargs=dict(link=link))


    def parse_date(self, response, link):
        title = response.xpath('//*[@class="h2 article-title"]/text()').extract()
        date = response.xpath('//*[@class="yoast-schema-graph"]').extract_first()

        pattern = re.compile('datePublished')
        initialIndex = re.search(pattern,date).end()
        date = date[initialIndex+3:initialIndex+13]

        print(link)
        maxCount = len(links)-1
        print(maxCount)
        global count

        if count < maxCount:
            titleList.append(title)
            linksList.append(link)
            datesList.append(date)
            count += 1
            print(count)

        if count == maxCount:
            print('in else')
            titleList.append(title)
            linksList.append(link)
            datesList.append(date)            
            yield Request('https://www.twosigma.com/topic/markets-economy/', \
                callback=self.parse_combine, cb_kwargs=dict(titleFinal=titleList, linkFinal=linksList, datesFinal=datesList))

    def parse_combine(self, response, titleFinal, linkFinal, datesFinal):
        items = FundInsightsTrackerItem()
        print('in parse combine')
        print(titleFinal)
        print(linkFinal)
        print(datesFinal)
        items = FundInsightsTrackerItem()

        titlesFinal = []
        len(titleFinal)
        for i in range(len(titleFinal)):
            t = titleFinal[i][0]
            titlesFinal.append(t)

        twosigma_item = []
        for i in range(len(titlesFinal)):
            tupTitle = titlesFinal[i]
            tupLink = linkFinal[i]
            tupDate = datesFinal[i]
            tup = (tupTitle, tupLink, tupDate)
            twosigma_item.append(tup)
            
        items['twosigma_item'] = twosigma_item
        yield items




