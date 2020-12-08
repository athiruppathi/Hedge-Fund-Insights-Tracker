from fund_insights_tracker.spiders import blackrock
from scrapy.crawler import CrawlerProcess
from fund_insights_tracker.spiders import bridgewater

process = CrawlerProcess()
process.crawl(blackrock.BlackrockSpider)
process.crawl(bridgewater.BridgewaterSpider)
process.start() 