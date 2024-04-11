from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea, QGroupBox, QPushButton
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt

from asyncWorker import Worker
from fetchData import fetchGameInfo, fetchChampPixmap, fetchItemPixmap

class matchHistoryGeneric(QScrollArea):
    def __init__(self, info, manager, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.threadPool = manager.threadPool
        self.IMAGE_LOCATION = IMAGE_LOCATION
        
        self.userData = info['userData']
        self.matchIndex = 20
        group = QGroupBox()
        
        boxlayout = QVBoxLayout()
        for GID in info['games'].keys():
            boxlayout.addWidget(Match(info['games'][GID], self.userData['PUUID'], self.manager, self.IMAGE_LOCATION))

        group.setLayout(boxlayout)
        self.setWidget(group)
        self.setFixedWidth(group.width() + 2)
        self.setWidgetResizable(True)

class matchHistory(matchHistoryGeneric):
    def __init__(self, info, manager, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(info, manager, IMAGE_LOCATION, *args, **kwargs)
        self.verticalScrollBar().valueChanged.connect(self.valueChanged, type=Qt.UniqueConnection)
        
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
        pixmap = QPixmap(self.IMAGE_LOCATION + 'champion/' + gameData[PUUID]['championName'] + '.png')
        pixmap = pixmap.scaled(50, 50, mode=Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        boxLayout.addWidget(label, 0, 0, -1, 1)
        
        #Loss/Win
        if gameData[PUUID]['won']:
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
        label = QLabel('CS: ' + str(gameData[PUUID]['totalMinionsKilled']))
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
            
            button = PlayerButton(player, gameData, fetchChampPixmap(gameData[player]['championName'], self.IMAGE_LOCATION), self.manager, self.IMAGE_LOCATION)
            
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
        
        self.playerName = gameData[PUUID]['gameName'] + " #" + gameData[PUUID]['tagLine']
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
        
class champMatchHistory(matchHistoryGeneric):
    def __init__(self, info, manager, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(info, manager, IMAGE_LOCATION, *args, **kwargs)