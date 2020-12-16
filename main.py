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

# Creates table for first time user
sqlCommand = '''dfasodfj'''     

c.execute(''' CREATE TABLE data (
        titles text,
        links text,
        dates text,
        source text) '''
)

def get_path(dataName):
    '''Gets the directory path of the scraped data. Must 
    call the function with dataName as a string'''
    currentDirectory = os.getcwd()
    partialPath = '\\' + dataName + '_data.json'
    fullPath = currentDirectory + partialPath
    return fullPath

def crawl_all():
    '''Crawls all websites, updates the master database with new entries, 
    and deletes the imported json files'''
    process = CrawlerProcess()
    process.crawl(blackrock.BlackrockSpider)
    process.crawl(bridgewater.BridgewaterSpider)
    process.crawl(carillon.CarillonSpider)
    process.crawl(kkr.KkrSpider)
    process.crawl(man.ManSpider)
    process.crawl(pimco.PimcoSpider)    
    process.crawl(schroders.SchrodersSpider)    
    process.crawl(twosigma.TwosigmaSpider)  
    process.crawl(williamblair.WilliamblairSpider)  
    process.start()     

    # Get all paths 
    fundsList = ['blackrock','bridgewater','carillon',  'kkr','man','pimco','schroders','twosigma','williamblair']
    pathsList = []
    for i in fundsList:
        pathsList.append(get_path(i))  
    

    # Import data
    #for i in paths


    # Add data to master database



    # Remove scraped data
    #for i in fundsList:
    #   os.remove(get_path(i))

crawl_all()
conn.commit()

conn.close()