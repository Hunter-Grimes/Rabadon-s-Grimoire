from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QStackedLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from LoadingIndicator import LoadingIndicator
from userTags import userTagsDisplay
from asyncWorker import Worker
from championStats import championStatsHandler
from matchHistory import matchHistory
from fetchData import fetchProfileInfo, fetchChampInfo


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
        
        self.profileWindow = QWidget()
        profileWindowLayout = QStackedLayout()
        self.profileWindow.setLayout(profileWindowLayout)
        self.profileWindow.layout().addWidget(ProfilePage(fetchProfileInfo(PUUID, self.BASE_URL), self, self.IMAGE_LOCATION))
        
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
        newPage = ProfilePage(info, self, self.IMAGE_LOCATION)
        self.addPage(newPage)

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
        label.setFixedSize(150, 150)
        pixmap = QPixmap(self.IMAGE_LOCATION + 'profileicon/' + str(userData['profileIcon']) + '.png')
        pixmap = pixmap.scaled(150, 150, mode=Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        layout.addWidget(label, 0, 0)
        
        #Username
        label = QLabel(userData['name'])
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
        
        #Real Champion Stats
        layout.addWidget(self.champStats, 2, 4, 1, 1)
        worker = Worker(fetchChampInfo, userData['PUUID'], self.manager.BASE_URL)
        worker.signals.result.connect(self.champStatsReady)
        self.threadPool.start(worker)
        
        self.setLayout(layout)
    
    def champStatsReady(self, info):
        gamesPlayed = info[0]
        championStats = info[1]
        champStats = championStatsHandler(gamesPlayed, championStats, self.manager, self.IMAGE_LOCATION)
        self.layout().replaceWidget(self.champStats, champStats)
        self.champStats.deleteLater()
        self.champStats = champStats