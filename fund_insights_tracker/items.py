# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class FundInsightsTrackerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    blackrock_item = scrapy.Field()
    bridgewater_item = scrapy.Field()
    carillon_item = scrapy.Field()
    kkr_item = scrapy.Field()
    man_item = scrapy.Field()
    pimco_item = scrapy.Field()
    schroders_item = scrapy.Field()
    twosigma_item = scrapy.Field()
    williamblair_item = scrapy.Field()