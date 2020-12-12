import sys
import json 
import sqlite3
import os 
import re 
import webbrowser
from fund_insights_tracker.spiders import blackrock, bridgewater, carillon, kkr, man, pimco, schroders, twosigma, williamblair
from scrapy.crawler import CrawlerProcess

conn = sqlite3.connect('master.db')
c = conn.cursor()


def get_path(dataName):
    '''Gets the directory path of the scraped data. Must 
    call the function with dataName as a string'''
    currentDirectory = os.getcwd()
    partialPath = '\\' + dataName + '_data.json'
    fullPath = currentDirectory + partialPath
    return fullPath

def load_all(data)



def import_data(data):
    json.load(get_data(data))
    return x = data


process = CrawlerProcess()
process.crawl(kkr.KkrSpider)
process.start() 

#os.remove(get_path('kkr'))
