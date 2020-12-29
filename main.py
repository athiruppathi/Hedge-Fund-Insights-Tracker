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

# Create main data table
c.execute('''CREATE TABLE IF NOT EXISTS main (
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
        isPatternMatch = re.match('<Request GET ', linkNew)
        if isPatternMatch:
            linkNew = linksPattern.sub('', linkNew)
            linkNew = linkNew[:-1]
        dateNew = dataDates1[i]
        tup = (titleNew,linkNew,dateNew)
        completeList.append(tup)

    # Add data to main data table
    c.executemany('INSERT INTO main VALUES (?,?,?)',completeList)
    c.execute('DELETE FROM main WHERE rowid NOT IN (SELECT min(rowid) FROM main GROUP BY titles, links)')

    # Remove old files 
    for i in fundsList:
        os.remove(get_path(i))

from PyQt5 import QtCore, QtGui, QtWidgets

#for i in c.execute(''' SELECT * FROM main'''):
    # add i[0] entry to table with a command that opens webbrower to 


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1032, 770)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.headingLabel = QtWidgets.QLabel(self.centralwidget)
        self.headingLabel.setGeometry(QtCore.QRect(10, 0, 271, 41))
        self.headingLabel.setObjectName("headingLabel")
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setGeometry(QtCore.QRect(730, 20, 298, 31))
        self.refreshButton.setObjectName("refreshButton")
        self.refreshButton.clicked.connect(self.refresh_command)


        self.tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.tabs.setGeometry(QtCore.QRect(10, 40, 1021, 711))
        self.tabs.setObjectName("tabs")
        self.All = QtWidgets.QWidget()
        self.All.setObjectName("All")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.All)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.allTable = QtWidgets.QTableWidget(self.All)
        self.allTable.setObjectName("allTable")
        self.allTable.setColumnCount(2)
        c.execute(''' SELECT * FROM main''')
        tableLen = len(c.fetchall())
        self.allTable.setRowCount(tableLen)
        self.allTable.setHorizontalHeaderLabels(['Article','Date'])
        columnHeader = self.allTable.horizontalHeader()
        columnHeader.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        columnHeader.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        rowPosition = self.allTable.rowCount()
        for i in c.execute(''' SELECT * FROM main'''):
            cellLabel = i[0]
            cellLink = i[1]
            cellDate = i[2]
            #self.allTable.setItem(rowPosition , 0, QtGui.QTableWidgetItem(cellLabel))
            #self.allTable.setItem(rowPosition , 1, QtGui.QTableWidgetItem(cellDate))

        self.horizontalLayout.addWidget(self.allTable)
        self.tabs.addTab(self.All, "")
        self.Favorites = QtWidgets.QWidget()
        self.Favorites.setObjectName("Favorites")
        self.favoritesTable = QtWidgets.QTableWidget(self.Favorites)
        self.favoritesTable.setGeometry(QtCore.QRect(10, 10, 971, 661))
        self.favoritesTable.setObjectName("favoritesTable")
        self.favoritesTable.setColumnCount(0) 
        self.favoritesTable.setRowCount(0) 
        self.tabs.addTab(self.Favorites, "") 
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.headingLabel.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">Hedge Fund Insights Tracker</span></p></body></html>"))
        self.refreshButton.setText(_translate("MainWindow", "Refresh"))
        self.tabs.setTabText(self.tabs.indexOf(self.All), _translate("MainWindow", "All"))
        self.tabs.setTabText(self.tabs.indexOf(self.Favorites), _translate("MainWindow", "Favorites"))

    def refresh_command(self):
        update_database()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

conn.commit()
conn.close()