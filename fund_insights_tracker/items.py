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
    blackrock_dates = scrapy.Field()
    bridgewater_titles = scrapy.Field()
    bridgewater_links = scrapy.Field()
    bridgewater_dates = scrapy.Field()
    schroders_titles = scrapy.Field()
    schroders_links = scrapy.Field()
    schroders_dates = scrapy.Field()
    man_titles = scrapy.Field()
    man_links = scrapy.Field()
    man_dates = scrapy.Field()
