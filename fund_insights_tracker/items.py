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

    williamblair_titles = scrapy.Field()
    williamblair_links = scrapy.Field()
    williamblair_dates = scrapy.Field()
    twosigma_titles = scrapy.Field()
    twosigma_links = scrapy.Field()
    twosigma_dates = scrapy.Field()
    pimco_titles = scrapy.Field()
    pimco_links = scrapy.Field()
    pimco_dates = scrapy.Field()
    carillon_titles = scrapy.Field()
    carillon_links = scrapy.Field()
    carillon_dates = scrapy.Field()
    kkr_titles = scrapy.Field()
    kkr_links = scrapy.Field()
    kkr_dates = scrapy.Field()