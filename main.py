from fund_insights_tracker.spiders import blackrock
from scrapy.crawler import CrawlerProcess
#from fund_insights_tracker.spiders import bridgewater
import os 

current_directory = os.getcwd()
partialPathBlackrock = '\\blackrock_data.json'
blackrockPath = current_directory + partialPathBlackrock

process = CrawlerProcess()
process.crawl(blackrock.BlackrockSpider)
process.start() 

#os.remove(blackrockPath)