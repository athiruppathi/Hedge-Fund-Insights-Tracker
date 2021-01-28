import scrapy
from ..items import FundInsightsTrackerItem


class TwosigmaSpider(scrapy.Spider):
    name = 'twosigma'
    start_urls = ['https://www.twosigma.com/topic/markets-economy/']

    def parse(self, response):
        items = FundInsightsTrackerItem()
        
        entry = response.xpath('//*[@class="postBlock"]')
        titles = entry.xpath('.//h3/a/text()').extract()
        links = entry.xpath('.//h3/a/@href').extract()

        dates = []
        for i in range(len(titles)):
            dates.append('---')

        # Combine data into tuples
        twosigma_item = []
        for i in range(len(titles)):
            tupTitle = titles[i]
            tupLink = links[i]
            tupDate = dates[i]
            tup = (tupTitle, tupLink, tupDate)
            twosigma_item.append(tup)

        items['twosigma_item'] = twosigma_item
        
        yield items