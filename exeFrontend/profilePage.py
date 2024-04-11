from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QStackedLayout, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from LoadingIndicator import LoadingIndicator
from userTags import userTagsDisplay
from asyncWorker import Worker
from championStats import championStatsHandler
from matchHistory import matchHistory
from champStatsPage import ChampStatsPageManager
from fetchData import fetchProfileInfo, fetchChampInfo, asyncUpdatePlayer, fetchChampInfoPage


class ProfilePageManager(QWidget):
    def __init__(self, PUUID, BASE_URL, threadpool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threadPool = threadpool
        
        self.fetchingPlayer = False
        self.playerWorker = None
        
        self.fetchingGames = False
        
        self.BASE_URL = BASE_URL
        self.IMAGE_LOCATION = 'dragontailData/14.5.1/img/'
        
        self.layout = QGridLayout()
        
        nextPage = QPushButton(">")
        prevPage = QPushButton("<")
        
        nextPage.clicked.connect(self.advancePage)
        prevPage.clicked.connect(self.retreatPage)
        
        nextPage.setFixedWidth(50)
        prevPage.setFixedWidth(50)
        
        self.layout.addWidget(prevPage, 0, 0)
        self.layout.addWidget(nextPage, 0, 1)
        
        self.loadingIndicator = LoadingIndicator(self)
        self.layout.addWidget(self.loadingIndicator, 0, 10)
        
        #user update button
        updateUserBtn = QPushButton("Update User")
        updateUserBtn.clicked.connect(self.updateBtnHandler)
        self.layout.addWidget(updateUserBtn, 0, 9)
        
        self.profileWindow = QWidget()
        profileWindowLayout = QStackedLayout()
        self.profileWindow.setLayout(profileWindowLayout)
        
        profileInfo = fetchProfileInfo(PUUID, self.BASE_URL)
        if profileInfo[1] != 201:
            self.updateFailed()
        
        self.profileWindow.layout().addWidget(ProfilePage(profileInfo[0], self, self.IMAGE_LOCATION))
        
        self.layout.addWidget(self.profileWindow, 1, 0, 1, -1)
        
        self.setLayout(self.layout)
    
    def setFetchPlayer(self):
        self.fetchingPlayer = False
    
    def setFetchGame(self):
        self.fetchingGames = False

    def createPage(self, PUUID):
        self.loadingIndicator.startAnimation()
        
        worker = Worker(fetchProfileInfo, PUUID, self.BASE_URL)
        self.fetchingPlayer = True
        self.playerWorker = worker
        
        worker.signals.result.connect(self.createPageHelper)
        worker.signals.finished.connect(self.setFetchPlayer)
        worker.signals.finished.connect(self.loadingIndicator.stopAnimation)
        
        self.threadPool.start(worker)
    
    def createPageHelper(self, info):
        if info[1] != 201:
            self.updateFailed()
        newPage = ProfilePage(info[0], self, self.IMAGE_LOCATION)
        self.addPage(newPage)
        
    def createChampStatsPage(self, PUUID, champName):
        self.loadingIndicator.startAnimation()

        worker = Worker(fetchChampInfoPage, PUUID, champName, self.BASE_URL)
        self.fetchingPlayer = True
        self.playerWorker = worker

        worker.signals.result.connect(self.createChampPageHelper)
        worker.signals.finished.connect(self.setFetchPlayer)
        worker.signals.finished.connect(self.loadingIndicator.stopAnimation)

        self.threadPool.start(worker)
        
    def createChampPageHelper(self, requestData):
        
        statsPage = ChampStatsPageManager(requestData, self, self.BASE_URL, self.threadPool, self.IMAGE_LOCATION)
        self.addPage(statsPage)
        

    def addPage(self, page):
        self.profileWindow.layout().insertWidget(self.profileWindow.layout().currentIndex() + 1, page)
        self.profileWindow.layout().setCurrentIndex(self.profileWindow.layout().currentIndex() + 1)
        
        if (self.profileWindow.layout().count() - 1) > self.profileWindow.layout().currentIndex():
            for i in range(self.profileWindow.layout().currentIndex() + 1, self.profileWindow.layout().count() - 1):
                self.profileWindow.layout().removeWidget(self.profileWindow.layout().itemAt(i).widget())
                self.profileWindow.layout().removeItem(self.profileWindow.layout().itemAt(i))     
        
    def advancePage(self):
        self.profileWindow.layout().setCurrentIndex(self.profileWindow.layout().currentIndex() + 1)
        
    def retreatPage(self):
        self.profileWindow.layout().setCurrentIndex(self.profileWindow.layout().currentIndex() - 1)
    
    def updateBtnHandler(self):
        page = self.profileWindow.layout().itemAt(self.profileWindow.layout().currentIndex()).widget()
        PUUID = page.info['userData']['PUUID']
        self.loadingIndicator.startAnimation()
        worker = Worker(asyncUpdatePlayer, PUUID, self.BASE_URL)
        self.fetchingPlayer = True
        self.playerWorker = worker
        
        worker.signals.result.connect(lambda: self.updatePage(PUUID))

        self.threadPool.start(worker)
       
    def updatePage(self, PUUID):
        self.loadingIndicator.startAnimation()
        
        worker = Worker(fetchProfileInfo, PUUID, self.BASE_URL)
        self.fetchingPlayer = True
        self.playerWorker = worker
        
        worker.signals.result.connect(lambda info: self.updatePageHelper(info, self.profileWindow.layout().currentIndex()))
        worker.signals.finished.connect(self.setFetchPlayer)
        worker.signals.finished.connect(self.loadingIndicator.stopAnimation)
        
        self.threadPool.start(worker)
    
    def updatePageHelper(self, info, index):
        if info[1] != 201:
            self.updateFailed()
        self.profileWindow.layout().itemAt(index).widget().deleteLater()
        newPage = ProfilePage(info[0], self, self.IMAGE_LOCATION)
        self.profileWindow.layout().insertWidget(index, newPage)
        
    def updateFailed(self):
        message = QMessageBox()
        message.setButtonText(QMessageBox.Ok, "Ok")
        message.setText("Update Failed")
        message.exec()
        

class ProfilePage(QWidget):
    def __init__(self, info, manager, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.info = info
        self.manager = manager
        self.threadPool = self.manager.threadPool
        self.IMAGE_LOCATION = IMAGE_LOCATION
        
        userData = info['userData']
        
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        #Match History
        scroll = matchHistory(info, self.manager, self.IMAGE_LOCATION)
        layout.addWidget(scroll, 2, 0, 3, 2)
        
        #Profile Icon
        label = QLabel()
        label.setStyleSheet("border: 3px solid black;")
        label.setFixedSize(150, 150)
        pixmap = QPixmap(self.IMAGE_LOCATION + 'profileicon/' + str(userData['profileIcon']) + '.png')
        pixmap = pixmap.scaled(150, 150, mode=Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        layout.addWidget(label, 0, 0)
        
        #Username
        label = QLabel(userData['gameName'] + " #" + userData['tagLine'])
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1, 0)
        
        #Tags
        tags = userTagsDisplay(userData['PUUID'], self.manager.BASE_URL, self.threadPool)
        layout.addWidget(tags, 0, 1, 1, 1, Qt.AlignLeft)
        
        #Rank Icon
        label = QLabel()
        pixmap = QPixmap(self.IMAGE_LOCATION + 'ranks/rank=' + userData['tier'] + '.png')
        pixmap = pixmap.scaled(150, 150, mode=Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 0, 4)
        
        #Rank Name
        label = QLabel(userData['tier'] + ' ' + userData['rank'])
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1, 4)
       
        #Placeholder for Champion Stats
        self.champStats = QWidget()
        self.champStats.setLayout(QVBoxLayout())
        loading = LoadingIndicator(self.manager)
        self.champStats.layout().addWidget(loading)
        self.champStats.layout().setAlignment(Qt.AlignCenter)
        loading.startAnimation()
        self.champStats.setFixedWidth(320)
        layout.addWidget(self.champStats, 2, 4, 1, 1)
        
        #Real Champion Stats
        worker = Worker(fetchChampInfo, userData['PUUID'], self.manager.BASE_URL)
        worker.signals.result.connect(self.champStatsReady)
        self.threadPool.start(worker)
        
        self.setLayout(layout)
    
    def champStatsReady(self, info):
        gamesPlayed = info[0]
        championStats = info[1]
        champStats = championStatsHandler(self.info['userData']['PUUID'], gamesPlayed, championStats, self.manager, self.IMAGE_LOCATION)
        self.layout().replaceWidget(self.champStats, champStats)
        self.champStats.deleteLater()
        self.champStats = champStats