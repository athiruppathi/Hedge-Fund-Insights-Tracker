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
#sqlCommand = '''dfasodfj'''     
#c.execute(''' CREATE TABLE data (
#        titles text,
#        links text,
#        dates text,
#        source text) '''
#)

def get_path(dataName):
    '''Gets the directory path of the scraped json data. Must 
    call the function with dataName as a string'''
    currentDirectory = os.getcwd()
    partialPath = '\\' + dataName + '_data.json'
    fullPath = currentDirectory + partialPath
    return fullPath

def crawl_all():
    '''Crawls all websites, imports data, updates the master database with new entries, 
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
    fundsList = ['blackrock','bridgewater','carillon', 'kkr','man','pimco','schroders','twosigma','williamblair']
    pathsList = []
    for i in fundsList:
        pathsList.append(get_path(i))  
    
    # Import data


    # Add data to master database



    # Remove json files
    #for i in fundsList:
    #   os.remove(get_path(i))

#crawl_all()

fundsList = ['blackrock','bridgewater','carillon',  'kkr','man','pimco','schroders','twosigma','williamblair']
pathsList = []
for i in fundsList:
    pathsList.append(get_path(i)) 

print(pathsList)

dataTitles = []
dataLinks = []
dataDates = []
for i in pathsList:
    with open(i) as f:
        data = json.load(f) # load json data
        dataDict = data[0]
        dictToList = list(dataDict.keys())
        titlesIndex = dictToList[0]
        dataName = titlesIndex[:-7] # get the name of fund to access dictionary

        dataT = dataDict.get( dataName + '_titles')
        dataTitles.append(dataT)
        dataL = dataDict.get(dataName + '_links')
        dataLinks.append(dataL)
        dataD = dataDict.get(dataName + '_dates')
        dataDates.append(dataD)

# Add data to master database - only add if it's new data
#c.execute('''SELECT ''')


# Remove json files
    for i in pathsList:
        os.remove(i)
print('arjun')
conn.commit()

conn.close()