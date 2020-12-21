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

# Create data table
c.execute('''CREATE TABLE IF NOT EXISTS data (
    titles text,
    links text,
    dates text
    )''')

# Create favorites table
c.execute('''CREATE TABLE IF NOT EXISTS favorites (
    titles text,
    links text,
    dates text
)''')

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
    
    dataTitles1 = []
    for i in dataTitles:
        for j in i:
            title = j
            dataTitles1.append(title)
    dataLinks1 = []
    for i in dataLinks:
        for j in i:
            link = j
            dataLinks1.append(link)
    dataDates1 = []
    for i in dataDates:
        for j in i:
            date = j
            dataDates1.append(date)         
    
    # Covert data into a list of tuples
    completeList = []
    for i in range(len(dataTitles1)):
        titleNew = dataTitles1[i]
        linkNew = dataLinks1[i]
        linksPattern = re.compile('<Request GET ')
        if re.match(linksPattern, linkNew) == True:
            linkNew = re.sub(linksPattern, '', linkNew)
            linkNew = linkNew[:-1]
        dateNew = dataDates1[i]
        tup = (titleNew,linkNew,dateNew)
        completeList.append(tup)

    print(len(completeList))

    # Add data to data table
    c.executemany('INSERT INTO data VALUES (?,?,?)', completeList)

    # Remove old files 
    for i in fundsList:
      os.remove(get_path(i))

update_database()

conn.commit()
conn.close()