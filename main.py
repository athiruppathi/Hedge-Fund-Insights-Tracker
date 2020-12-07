from fund_insights_tracker.spiders import blackrock
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()
process.crawl(blackrock.BlackrockSpider)
process.start()