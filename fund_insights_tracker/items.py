# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FundInsightsTrackerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    blackrock_titles = scrapy.Field()
    blackrock_links = scrapy.Field()
    bridgewater_titles = scrapy.Field()
    bridgewater_links = scrapy.Field()
