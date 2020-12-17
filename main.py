import sys
import PyQt5
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
sqlCommand = '''SELECT name FROM master.db WHERE type='table' AND name='{data}';'''
if sqlCommand == False:
    c.execute(''' CREATE TABLE data (
        titles text,
        links text,
        dates text,
        source text) '''
    )

def get_path(dataName):
    '''Gets the directory path of the scraped json data. Must 
    call the function with dataName as a string'''
    currentDirectory = os.getcwd()
    partialPath = '\\' + dataName + '_data.json'
    fullPath = currentDirectory + partialPath
    return fullPath

def crawl_all():
    '''Crawls all websites'''
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

def update_database():
    '''imports data, updates the master database with new entries, 
    and deletes the imported json files'''
    
    # Delete old data if it exists
    fundsList = ['blackrock','bridgewater','carillon',  'kkr','man','pimco','schroders','twosigma','williamblair']
    for i in fundsList:
        if os.path.isfile(get_path(i)) == True:
            os.remove(get_path(i))

    crawl_all()

    # Import Data
    pathsList = []
    for i in fundsList:
        pathsList.append(get_path(i)) 

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

    # Convert data into a list of tuples
    completeList = []  # is a list of tuples
    for i in dataTitles:
        for j in dataLinks:
            for k in dataDates:
                dataTuples = (i,j,k)
                completeList.append(dataTuples)
    
    print(completeList[0][0])
    print(type(completeList))

    # Add data to master database
    #for i in completeList:
    #   c.executemany('INSERT INTO data VALUES (?,?,?,?)', data)

    # Remove old files 
    for i in fundsList:
       os.remove(get_path(i))

update_database()

conn.commit()
conn.close()