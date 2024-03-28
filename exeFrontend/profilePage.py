from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea, QGroupBox, QPushButton, QStackedLayout
from PySide6.QtGui import QPixmap, QColor, QIcon
from PySide6.QtCore import Qt
import requests


class ProfilePageManager(QWidget):
    def __init__(self, PUUID, BASE_URL, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QGridLayout()
        self.BASE_URL = BASE_URL
        self.IMAGE_LOCATION = 'dragontailData/14.5.1/img/'
        
        nextPage = QPushButton("Next")
        prevPage = QPushButton("Back")
        
        nextPage.clicked.connect(self.advancePage)
        prevPage.clicked.connect(self.retreatPage)
        
        self.layout.addWidget(prevPage, 0, 0)
        self.layout.addWidget(nextPage, 0, 1)
        
        self.profileWindow = QWidget()
        profileWindowLayout = QStackedLayout()
        self.profileWindow.setLayout(profileWindowLayout)
        self.profileWindow.layout().addWidget(ProfilePage(PUUID, self, self.BASE_URL, self.IMAGE_LOCATION))
        
        self.layout.addWidget(self.profileWindow, 1, 0, 1, -1)
        
        self.setLayout(self.layout)
        

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
    def __init__(self, PUUID, manager, BASE_URL, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.BASE_URL = BASE_URL
        self.IMAGE_LOCATION = IMAGE_LOCATION
        
        userData = requests.get(self.BASE_URL + '/user/by-PUUID/' + str(PUUID)).json()
        requests.put(self.BASE_URL + '/update-user/' + str(PUUID))
        
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        scroll = MatchHistory(userData, self.manager, self.BASE_URL, self.IMAGE_LOCATION)
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
        
        self.setLayout(layout)

      
class MatchHistory(QScrollArea):
    def __init__(self, userData, manager, BASE_URL, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.BASE_URL = BASE_URL
        self.IMAGE_LOCATION = IMAGE_LOCATION
        
        self.userData = userData
        self.matchIndex = 20
        group = QGroupBox()
        
        self.verticalScrollBar().valueChanged.connect(self.valueChanged, type=Qt.UniqueConnection)
        
        boxlayout = QVBoxLayout()
        for id in requests.get(self.BASE_URL + '/game-id/x-x/' + self.userData['PUUID'] + '/0/20').json():
            boxlayout.addWidget(Match(id, self.userData['PUUID'], self.manager, self.BASE_URL, self.IMAGE_LOCATION))

        group.setLayout(boxlayout)
        self.setWidget(group)
        self.setFixedWidth(group.width() + 2)
        self.setWidgetResizable(True)
        
    def valueChanged(self, value):
        if value == self.verticalScrollBar().maximum():
            self.add_lines(5)

    def add_lines(self, n):
        for id in requests.get(self.BASE_URL + '/game-id/x-x/' + self.userData['PUUID'] + '/' + str(self.matchIndex) + '/' + str(self.matchIndex + n)).json():
            self.widget().layout().addWidget(Match(id, self.userData['PUUID'], self.manager, self.BASE_URL, self.IMAGE_LOCATION))
        self.matchIndex += n
            
             
class Match(QWidget):    
    def __init__(self, GID, PUUID, manager, BASE_URL, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.BASE_URL = BASE_URL
        self.IMAGE_LOCATION = IMAGE_LOCATION

        gameData = requests.get(self.BASE_URL + '/game-data/all/' + GID).json()
        
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
        itemBox = ItemDisplay(PUUID, gameData, self.manager, self.BASE_URL, self.IMAGE_LOCATION)
        boxLayout.addWidget(itemBox, 0, 3, -1, 1)
        
        #Champions
        champBox = ChampDisplay(gameData, self.manager, self.BASE_URL, self.IMAGE_LOCATION)
        boxLayout.addWidget(champBox, 0, 4, -1, 1)
        
        box.setLayout(boxLayout)
        layout.addWidget(box)
        self.setLayout(layout)
        

class ItemDisplay(QGroupBox):
    def __init__(self, PUUID, gameData, manager, BASE_URL, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.BASE_URL = BASE_URL
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
    def __init__(self, gameData, manager, BASE_URL, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.BASE_URL = BASE_URL
        self.IMAGE_LOCATION = IMAGE_LOCATION
        
        champs = QGridLayout()
        
        for i, player in enumerate(list(gameData.keys())):
            
            button = PlayerButton(player, gameData, fetchChampPixmap(gameData[player]['champion_name'], self.IMAGE_LOCATION), self.manager, self.BASE_URL, self.IMAGE_LOCATION)
            
            if i < 5:
                champs.addWidget(button, 0, i)
            else:
                champs.addWidget(button, 1, i - 5)
        
        self.setLayout(champs)
        
      
class PlayerButton(QPushButton):
    def __init__(self, PUUID, gameData, pixmap, manager, BASE_URL, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.BASE_URL = BASE_URL
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
        self.manager.addPage(ProfilePage(self.PUUID, self.manager, self.BASE_URL, self.IMAGE_LOCATION))

 
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