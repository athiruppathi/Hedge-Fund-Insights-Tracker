import scrapy
from urllib.parse import urljoin
from ..items import FundInsightsTrackerItem

class ManSpider(scrapy.Spider):
    name = 'man'
    start_urls = ['https://www.man.com/maninstitute/']
    custom_settings = {
        'FEED_FORMAT':'json',
        'FEED_URI':'man.json'
    }

    def parse(self, response):
        items = FundInsightsTrackerItem()

        entry = response.css('.col-12.col-md-6.col-lg-4.teaser__wrap.teaser__wrap--small')
        titles = entry.xpath('.//*[@class="teaser__content"]/h2/text()').extract()
        dates = entry.xpath('//*[@class="details__date"]/text()')
        dates_list = dates[2:14].extract()

        links = entry.xpath('.//a/@href')
        absolute_url_list = []
        for link in links:
            absolute_url = response.follow(link, callback=self.parse)
            absolute_url_list.append(absolute_url)   

        items['man_titles'] = titles
        items['man_dates'] = dates_list
        items['man_links'] = absolute_url_list
        yield items



