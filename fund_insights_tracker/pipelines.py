# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

conn = sqlite3.connect('master.db')
c = conn.cursor()

class FundInsightsTrackerPipeline:
    def process_item(self, item, spider):
                   
        c.execute('SELECT (titles) FROM main') 
        dbResult = c.fetchall()
        adapter = ItemAdapter(item)

        titleCheckList = []                  # this list is used to check whether the title exists in the database
        for i in range(len(dbResult)):
            dbTitle = dbResult[i][0]
            titleCheckList.append(dbTitle)

        #itemList = ['blackrock_item','bridgewater_item','carillon_item','kkr_item','man_item','pimco_item','schroders_item','twosigma_item','williamblair_item']

        itemResult = adapter.get('man_item')

        print(itemResult)
        for i in range(len(itemResult)):
            itemTitle = itemResult[i][0]
            if itemTitle not in titleCheckList:
                itemLink = itemResult[i][1]
                itemDate = itemResult[i][2]
                print(itemResult[0])
                c.execute('INSERT INTO main VALUES (?,?,?)', (str(itemTitle),str(itemLink),str(itemDate)))
                conn.commit()
                print('added new row to database')
            else: 
                print('not added to database')
