import scrapy
from ..items import FundInsightsTrackerItem


class TwosigmaSpider(scrapy.Spider):
    name = 'twosigma'
    start_urls = ['https://www.twosigma.com/topic/markets-economy/']

    custom_settings = {
        'FEED_FORMAT':'json',
        'FEED_URI':'twosigma_data.json'
    }

    def parse(self, response):
        items = FundInsightsTrackerItem()
        
        entry = response.xpath('//*[@class="postBlock"]')
        titles = entry.xpath('.//h3/a/text()').extract()
        links = entry.xpath('.//h3/a/@href').extract()

        dates = []
        for i in range(len(titles)):
            dates.append('---')

        items['twosigma_titles'] = titles
        items['twosigma_links'] = links
        items['twosigma_dates'] = dates
        yield items