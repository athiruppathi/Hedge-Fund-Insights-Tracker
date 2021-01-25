import sys
import PyQt5
import json 
import sqlite3
import os 
import re 
import webbrowser
from fund_insights_tracker.spiders import blackrock, bridgewater, carillon, kkr, man, pimco, schroders, twosigma, williamblair
from scrapy.crawler import CrawlerProcess
import tkinter as tk

root = tk.Tk()
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

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
    
    #print(dataTitles[-1])
    dataTitles1 = []
    for i in dataTitles:
        for j in i:
            if j not in dataTitles1:
                dataTitles1.append(j)
    dataLinks1 = []
    for i in dataLinks:
        for j in i:
            if j not in dataLinks1:
                dataLinks1.append(j)
    dataDates1 = []
    for i in dataDates:
        for j in i:
            dataDates1.append(j)
    
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
    c.executemany('INSERT INTO main VALUES (?,?,?)', completeList)
    c.execute('DELETE FROM main WHERE rowid NOT IN (SELECT min(rowid) FROM main GROUP BY titles, links)')
    conn.commit()

    # Remove old files 
    for i in fundsList:
       os.remove(get_path(i))

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        if screenWidth >= 1920 and screenHeight >= 1080:
            pix1 = 771
            pix2 = 721
        else:
            pix1 = 1497
            pix2 = 1047          

        v1 = pix1
        v2 = pix2 - 15
        form1 = pix1 + 3
        form2 = pix2 + 4

        Form.resize(form1, form2)
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, pix1, pix2))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.allTab = QtWidgets.QWidget()
        self.allTab.setObjectName("allTab")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.allTab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, v1, v2))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.allTabVerticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.allTabVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.allTabVerticalLayout.setObjectName("allTabVerticalLayout")
        self.allTable = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.allTable.setObjectName("allTable")
        self.allTable.setColumnCount(2)
        c.execute(''' SELECT * FROM main''')
        allTableLen = len(c.fetchall())
        self.allTable.setRowCount(allTableLen)
        self.allTable.setHorizontalHeaderLabels(['Article','Date'])
        columnHeader = self.allTable.horizontalHeader()
        columnHeader.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        columnHeader.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.allTabVerticalLayout.addWidget(self.allTable)
        self.tabWidget.addTab(self.allTab, "")
        self.favoritesTab = QtWidgets.QWidget()
        self.favoritesTab.setObjectName("favoritesTab")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.favoritesTab)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, v1, v2))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.favoritesVerticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.favoritesVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.favoritesVerticalLayout.setObjectName("favoritesVerticalLayout")
        self.favoritesTable = QtWidgets.QTableWidget(self.verticalLayoutWidget_2)
        self.favoritesTable.setObjectName("favoritesTable")
        self.favoritesTable.setColumnCount(2)
        favColumnHeader = self.favoritesTable.horizontalHeader()
        favColumnHeader.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        favColumnHeader.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        c.execute(''' SELECT * FROM favorites''')
        favTableLen = len(c.fetchall())       
        self.favoritesTable.setRowCount(favTableLen)
        self.favoritesTable.setHorizontalHeaderLabels(['Article','Date'])
        self.favoritesVerticalLayout.addWidget(self.favoritesTable)
        self.tabWidget.addTab(self.favoritesTab, "")
        self.gridLayout.addWidget(self.tabWidget, 3, 0, 1, 1)
        self.headingLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headingLabel.sizePolicy().hasHeightForWidth())
        self.headingLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.headingLabel.setFont(font)
        self.headingLabel.setObjectName("headingLabel")
        self.gridLayout.addWidget(self.headingLabel, 1, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.refreshButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.refreshButton.setObjectName("refreshButton")
        self.refreshButton.clicked.connect(self.refresh_command)
        self.gridLayout.addWidget(self.refreshButton, 2, 0, 1, 1, QtCore.Qt.AlignLeft)
        
        # Populate the all table
        rowPosition = 0 
        for i in c.execute(''' SELECT * FROM main'''):
           cellTitle = QtWidgets.QTableWidgetItem(i[0])
           cellDate = QtWidgets.QTableWidgetItem(i[2])
           self.allTable.setItem(rowPosition , 0, cellTitle)
           self.allTable.setItem(rowPosition , 1, cellDate)
           rowPosition += 1

        self.allTable.cellDoubleClicked.connect(self.open_link)  # connects to open_link function
        self.allTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers) # make table cells non-editable
        self.favoritesTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def open_link(self, row, column):
        item = self.allTable.item(row,column)
        itemTxt = item.text() 
        c.execute('SELECT links FROM main WHERE titles = (?)', (itemTxt,))
        result = c.fetchall()
        url = result[0][0]
        webbrowser.open(url, new=0)

    def refresh_command(self):
        update_database()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.allTab), _translate("Form", "All"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.favoritesTab), _translate("Form", "Favorites"))
        self.headingLabel.setText(_translate("Form", "Hedge Fund Insights"))
        self.refreshButton.setText(_translate("Form", "Refresh"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
