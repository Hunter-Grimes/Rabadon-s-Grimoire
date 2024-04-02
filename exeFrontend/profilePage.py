from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea, QGroupBox, QPushButton, QStackedLayout, QProgressBar
from PySide6.QtGui import QPixmap, QColor, QIcon, QMovie
from PySide6.QtCore import Qt
import requests
from asyncWorker import Worker

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


class LoadingIndicator(QLabel):
    def __init__(self, manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        
        self.setFixedSize(20, 20)
        self.movie = QMovie('exeFrontend/loading.gif')
        self.movie.setScaledSize(self.size())
        self.setMovie(self.movie)
        
    def startAnimation(self):
        self.show()
        self.movie.start()
        
    def stopAnimation(self):
        if (not self.manager.fetchingPlayer) and (not self.manager.fetchingGames):
            self.movie.stop()
            self.hide()


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
        
        scroll = MatchHistory(info, self.manager, self.IMAGE_LOCATION)
        layout.addWidget(scroll, 2, 0, 1, 2)
        
        label = QLabel()
        pixmap = QPixmap(self.IMAGE_LOCATION + 'profileicon/' + str(userData['profileIcon']) + '.png')
        pixmap = pixmap.scaled(150, 150, mode=Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        layout.addWidget(label, 0, 0)
        
        label = QLabel(userData['name'])
        layout.addWidget(label, 1, 0)
        
        label = QLabel()
        pixmap = QPixmap(self.IMAGE_LOCATION + 'ranks/rank=' + userData['tier'] + '.png')
        pixmap = pixmap.scaled(150, 150, mode=Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 0, 3)
        
        label = QLabel(userData['tier'] + ' ' + userData['rank'])
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1, 3)
        
        self.champStats = QScrollArea()
        layout.addWidget(self.champStats, 2, 3, 1, 1)
        worker = Worker(fetchChampInfo, userData['PUUID'], self.manager.BASE_URL)
        worker.signals.result.connect(self.champStatsReady)
        self.threadPool.start(worker)
        
        self.setLayout(layout)
    
    def champStatsReady(self, info):
        gamesPlayed = info[0]
        champStats = info[1]
        self.champStats = championStatsHandler(gamesPlayed, champStats, self.manager, self.IMAGE_LOCATION)
        self.layout().addWidget(self.champStats, 2, 3, 1, 1)


class championStatsHandler(QWidget):
    def __init__(self, totalGames, champStats, manager, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.championStats = championStats(totalGames, champStats, manager, IMAGE_LOCATION)
        layout = QGridLayout()
        
        self.sortedBy = None
        
        self.champNameButton = QPushButton("Name")
        self.gamesPlayedButton = QPushButton("Num Games Played")
        self.winPercentageButton = QPushButton("Win %")
        
        self.champNameButton.pressed.connect(self.sortByName)
        self.gamesPlayedButton.pressed.connect(self.sortByGamesPlayed)
        self.winPercentageButton.pressed.connect(self.sortByWinPercentage)
        
        layout.addWidget(self.champNameButton, 0, 0)
        layout.addWidget(self.gamesPlayedButton, 0, 1)
        layout.addWidget(self.winPercentageButton, 0, 2)
        layout.addWidget(self.championStats, 1, 0, 1, -1)
        
        self.sortByGamesPlayed()
        
        self.setLayout(layout)
        
    def sortByName(self):
        order = []
        for item in range(self.championStats.widget().layout().count()):
            order.append((self.championStats.widget().layout().itemAt(item).widget(), self.championStats.widget().layout().itemAt(item).widget().championName))
        
        if self.sortedBy == "name":
            order.sort(key=lambda x: x[1], reverse=True)
        else:
            order.sort(key=lambda x: x[1])
        
        layout = QVBoxLayout()
        
        for item in order:
            layout.addWidget(item[0])
            
        newWidget = QGroupBox()
        newWidget.setLayout(layout)
        
        self.championStats.setWidget(newWidget)
        
        if self.sortedBy == "name":
            self.sortedBy = "nameReverse"
        else:
            self.sortedBy = "name"
    
    def sortByGamesPlayed(self):
        order = []
        for item in range(self.championStats.widget().layout().count()):
            order.append((self.championStats.widget().layout().itemAt(item).widget(), self.championStats.widget().layout().itemAt(item).widget().champGamesPlayed))
        
        if self.sortedBy == "gamesPlayed":
            order.sort(key=lambda x: x[1])
        else:
            order.sort(key=lambda x: x[1], reverse=True)
        
        layout = QVBoxLayout()
        
        for item in order:
            layout.addWidget(item[0])
            
        newWidget = QGroupBox()
        newWidget.setLayout(layout)
        
        self.championStats.setWidget(newWidget)
        
        if self.sortedBy == "gamesPlayed":
            self.sortedBy = "gamesPlayedReverse"
        else:
            self.sortedBy = "gamesPlayed"
            
    def sortByWinPercentage(self):
        order = []
        for item in range(self.championStats.widget().layout().count()):
            order.append((self.championStats.widget().layout().itemAt(item).widget(), self.championStats.widget().layout().itemAt(item).widget().winPercentage))
        
        if self.sortedBy == "winPercentage":
            order.sort(key=lambda x: x[1])
        else:
            order.sort(key=lambda x: x[1], reverse=True)
        
        layout = QVBoxLayout()
        
        for item in order:
            layout.addWidget(item[0])
            
        newWidget = QGroupBox()
        newWidget.setLayout(layout)
        
        self.championStats.setWidget(newWidget)
        
        if self.sortedBy == "winPercentage":
            self.sortedBy = "winPercentageReverse"
        else:
            self.sortedBy = "winPercentage"

class championStats(QScrollArea):
    def __init__(self, totalGames, champStats, manager, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.totalGames = totalGames
        self.champStats = champStats
        self.manager = manager
        self.threadPool = manager.threadPool
        self.IMAGE_LOCATION = IMAGE_LOCATION
        
        group = QGroupBox()
        
        boxlayout = QVBoxLayout()
        for champ in champStats.keys():
            boxlayout.addWidget(champStatsChip(self.totalGames, champ, self.champStats[champ], self.manager, self.IMAGE_LOCATION))

        group.setLayout(boxlayout)
        self.setWidget(group)
        self.setFixedWidth(group.width() + 2)
        self.setWidgetResizable(True)
        


class champStatsChip(QWidget):
    def __init__(self, totalGames, championName, stats, manager, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.totalGames = totalGames
        
        self.championName = championName
        self.champGamesPlayed = stats['gamesPlayed']
        self.winPercentage = stats['wins'] / stats['gamesPlayed']
        
        self.stats = stats
        self.manager = manager
        self.IMAGE_LOCATION = IMAGE_LOCATION
        
        layout = QVBoxLayout()
        box = QGroupBox()
        box.setFixedSize(300, 85)
        boxLayout = QGridLayout()
        
        #Champion Icon
        label = QLabel()
        pixmap = QPixmap(self.IMAGE_LOCATION + 'champion/' + self.championName + '.png')
        pixmap = pixmap.scaled(40, 40, mode=Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        boxLayout.addWidget(label, 0, 0, 4, 1, alignment=Qt.AlignCenter)
        
        #Champion Name
        label = QLabel(self.championName)
        label.setAlignment(Qt.AlignCenter)
        boxLayout.addWidget(label, 1, 1, 1, 1, alignment=Qt.AlignCenter)
        
        #KDA
        kda = str(self.stats['avgKill']) + '/' + str(self.stats['avgDeath']) + '/' + str(self.stats['avgAssist'])
        label = QLabel(kda)
        label.setAlignment(Qt.AlignCenter)
        boxLayout.addWidget(label, 2, 1, 1, 1, alignment=Qt.AlignCenter)
        
        #Games Played
        gamesPlayed = QProgressBar()
        gamesPlayed.setMaximum(self.totalGames)
        gamesPlayed.setValue(self.stats['gamesPlayed'])
        boxLayout.addWidget(gamesPlayed, 1, 2, 1, 1, alignment=Qt.AlignCenter)
        
        numGamesPlayed = QLabel(str(self.stats['gamesPlayed']))
        numGamesPlayed.setAlignment(Qt.AlignCenter)
        boxLayout.addWidget(numGamesPlayed, 2, 2, 1, 1, alignment=Qt.AlignCenter)
        
        #Games Won
        gamesWon = QProgressBar()
        gamesWon.setMaximum(self.stats['gamesPlayed'])
        gamesWon.setValue(self.stats['wins'])
        boxLayout.addWidget(gamesWon, 1, 3, 1, 1, alignment=Qt.AlignCenter)
        
        numGamesWon = QLabel(str(round(self.stats['wins'] / self.stats['gamesPlayed'], 4) * 100) + '%')
        numGamesWon.setAlignment(Qt.AlignCenter)
        boxLayout.addWidget(numGamesWon, 2, 3, 1, 1, alignment=Qt.AlignCenter)
        
        box.setLayout(boxLayout)
        layout.addWidget(box)
        self.setLayout(layout)
        
        
class MatchHistory(QScrollArea):
    def __init__(self, info, manager, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.threadPool = manager.threadPool
        self.IMAGE_LOCATION = IMAGE_LOCATION
        
        self.userData = info['userData']
        self.matchIndex = 20
        group = QGroupBox()
        
        self.verticalScrollBar().valueChanged.connect(self.valueChanged, type=Qt.UniqueConnection)
        
        boxlayout = QVBoxLayout()
        for GID in info['games'].keys():
            boxlayout.addWidget(Match(info['games'][GID], self.userData['PUUID'], self.manager, self.IMAGE_LOCATION))

        group.setLayout(boxlayout)
        self.setWidget(group)
        self.setFixedWidth(group.width() + 2)
        self.setWidgetResizable(True)
        
    def valueChanged(self, value):
        if value == self.verticalScrollBar().maximum():
            self.add_lines(5)

    def add_lines(self, n):
        self.manager.loadingIndicator.startAnimation()
        self.manager.fetchingGames = True
        
        worker = Worker(fetchGameInfo, self.userData, self.manager.BASE_URL, '/' + str(self.matchIndex) + '/' + str(self.matchIndex + n))
        worker.signals.result.connect(self.add_lines_finished)
        
        worker.signals.finished.connect(self.manager.setFetchGame)
        worker.signals.finished.connect(self.manager.loadingIndicator.stopAnimation)
        worker.signals.finished.connect(self.incrementMatchIndex(n))
        
        self.threadPool.start(worker)
        
    def add_lines_finished(self, info):
        for id in info.keys():
            self.widget().layout().addWidget(Match(info[id], self.userData['PUUID'], self.manager, self.IMAGE_LOCATION))
    
    def incrementMatchIndex(self, n):
        self.matchIndex += n

             
class Match(QWidget):    
    def __init__(self, gameData, PUUID, manager, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.IMAGE_LOCATION = IMAGE_LOCATION
        
        layout = QVBoxLayout()
        box = QGroupBox()
        box.setFixedSize(600, 150)
        boxLayout = QGridLayout()
        
        #Champion Icon
        label = QLabel()
        pixmap = QPixmap(self.IMAGE_LOCATION + 'champion/' + gameData[PUUID]['champion_name'] + '.png')
        pixmap = pixmap.scaled(50, 50, mode=Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        boxLayout.addWidget(label, 0, 0, -1, 1)
        
        #Loss/Win
        if gameData[PUUID]['won_game']:
            label = QLabel("Victory")
            label.setStyleSheet("color: green")
        else:
            label = QLabel("Defeat")
            label.setStyleSheet("color: red")
        
        boxLayout.addWidget(label, 0, 1, -1, 1)
        
        #K/D/A
        label = QLabel(str(gameData[PUUID]['kills']) + '/' + str(gameData[PUUID]['deaths']) + '/' + str(gameData[PUUID]['assists']))
        boxLayout.addWidget(label, 0, 2)
        
        #CS
        label = QLabel('CS: ' + str(gameData[PUUID]['total_minions']))
        boxLayout.addWidget(label, 1, 2)
        
        #Items
        itemBox = ItemDisplay(PUUID, gameData, self.manager, self.IMAGE_LOCATION)
        boxLayout.addWidget(itemBox, 0, 3, -1, 1)
        
        #Champions
        champBox = ChampDisplay(gameData, self.manager, self.IMAGE_LOCATION)
        boxLayout.addWidget(champBox, 0, 4, -1, 1)
        
        box.setLayout(boxLayout)
        layout.addWidget(box)
        self.setLayout(layout)
        

class ItemDisplay(QGroupBox):
    def __init__(self, PUUID, gameData, manager, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.IMAGE_LOCATION = IMAGE_LOCATION
        
        items = QGridLayout()
        
        for item in range(6):
            label = QLabel()
            pixmap = fetchItemPixmap(gameData[PUUID]['item' + str(item)], self.IMAGE_LOCATION)
            label.setPixmap(pixmap)
            
            if item < 3:
                items.addWidget(label, 0, item)
            else:
                items.addWidget(label, 1, item - 3)
        
        self.setLayout(items)


class ChampDisplay(QGroupBox):
    def __init__(self, gameData, manager, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.IMAGE_LOCATION = IMAGE_LOCATION
        
        champs = QGridLayout()
        
        for i, player in enumerate(list(gameData.keys())):
            
            button = PlayerButton(player, gameData, fetchChampPixmap(gameData[player]['champion_name'], self.IMAGE_LOCATION), self.manager, self.IMAGE_LOCATION)
            
            if i < 5:
                champs.addWidget(button, 0, i)
            else:
                champs.addWidget(button, 1, i - 5)
        
        self.setLayout(champs)
        
      
class PlayerButton(QPushButton):
    def __init__(self, PUUID, gameData, pixmap, manager, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.IMAGE_LOCATION = IMAGE_LOCATION
        
        self.playerName = gameData[PUUID]['name']
        self.setToolTip(self.playerName)
        
        self.PUUID = PUUID
        self.pixmap = pixmap
        Icon = QIcon()
        
        Icon.addPixmap(self.pixmap)
        self.setIcon(Icon)
        
        self.setIconSize(self.pixmap.size())
        self.setFixedSize(self.pixmap.size())

        self.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        self.manager.createPage(self.PUUID)

 
def fetchItemPixmap(itemID, IMAGE_LOCATION):
    if itemID == 0:
        pixmap = QPixmap(30, 30)
        pixmap.fill(QColor(100, 100, 100))
        return pixmap
    
    pixmap = QPixmap(IMAGE_LOCATION + 'item/' + str(itemID) + '.png').scaled(30, 30, mode=Qt.SmoothTransformation)
    
    return pixmap


def fetchChampPixmap(champName, IMAGE_LOCATION):
    pixmap = QPixmap(IMAGE_LOCATION + 'champion/' + str(champName) + '.png').scaled(30, 30, mode=Qt.SmoothTransformation)

    return pixmap


def fetchProfileInfo(PUUID, BASE_URL):
    userData = requests.get(BASE_URL + '/user/by-PUUID/' + str(PUUID)).json()
    requests.put(BASE_URL + '/update-user/' + str(PUUID))
    games = fetchGameInfo(userData, BASE_URL, '/0/20')
    
    data = {
        "userData": userData,
        "games": games
    }
    
    return data


def fetchGameInfo(userData, BASE_URL, indexes):
    gamesIDS = requests.get(BASE_URL + '/game-id/x-x/' + userData['PUUID'] + indexes).json()
    games = dict()
    for game in gamesIDS:
        gameData = requests.get(BASE_URL + '/game-data/all/' + game).json()
        games[game] = gameData

    return games


def fetchChampInfo(PUUID, BASE_URL):
    champStats = requests.get(BASE_URL + '/champ-stats/' + PUUID).json()
    gamesPlayed = requests.get(BASE_URL + '/user/games-played/' + PUUID).json()

    return gamesPlayed, champStats