from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea, QGroupBox
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt
import requests

class ProfilePage(QWidget):
    BASE_URL = "http://127.0.0.1:5000"
    IMAGE_LOCATION = 'dragontailData/14.5.1/img/'
    def __init__(self, PUUID, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        userData = requests.get(self.BASE_URL + '/user/by-PUUID/' + str(PUUID)).json()
        requests.put(self.BASE_URL + '/update-user/' + str(PUUID))
        
        
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        
        scroll = MatchHistory(userData)
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
    BASE_URL = "http://127.0.0.1:5000"
    IMAGE_LOCATION = 'dragontailData/14.5.1/img/'
    
    def __init__(self, userData, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.userData = userData
        self.matchIndex = 20
        group = QGroupBox()
        
        
        self.verticalScrollBar().valueChanged.connect(self.valueChanged, type=Qt.UniqueConnection)
        
        boxlayout = QVBoxLayout()
        for id in requests.get(self.BASE_URL + '/game-id/x-x/' + self.userData['PUUID'] + '/0/20').json():
            boxlayout.addWidget(Match(id, self.userData['PUUID']))

        group.setLayout(boxlayout)
        self.setWidget(group)
        self.setFixedWidth(group.width() + 2)
        self.setWidgetResizable(True)

        
    def valueChanged(self, value):
        if value == self.verticalScrollBar().maximum():
            self.add_lines(5)


    def add_lines(self, n):
        for id in requests.get(self.BASE_URL + '/game-id/x-x/' + self.userData['PUUID'] + '/' + str(self.matchIndex) + '/' + str(self.matchIndex + n)).json():
            self.widget().layout().addWidget(Match(id, self.userData['PUUID']))
        self.matchIndex += n
            
             
class Match(QWidget):
    IMAGE_LOCATION = 'dragontailData/14.5.1/img/'
    BASE_URL = "http://127.0.0.1:5000"
    
    def __init__(self, GID, PUUID, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #matchData = requests.get(self.BASE_URL + '/game-data/by-Player/' + GID + '/' + PUUID).json()
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
        itemBox = QGroupBox()
        items = QGridLayout()
        
        label = QLabel()
        pixmap = self.fetchItemPixmap(gameData[PUUID]['item0'])
        label.setPixmap(pixmap)
        items.addWidget(label, 0, 0)
        
        label = QLabel()
        pixmap = self.fetchItemPixmap(gameData[PUUID]['item1'])
        label.setPixmap(pixmap)
        items.addWidget(label, 0, 1)
        
        label = QLabel()
        pixmap = self.fetchItemPixmap(gameData[PUUID]['item2'])
        label.setPixmap(pixmap)
        items.addWidget(label, 0, 2)
        
        label = QLabel()
        pixmap = self.fetchItemPixmap(gameData[PUUID]['item3'])
        label.setPixmap(pixmap)
        items.addWidget(label, 1, 0)
        
        label = QLabel()
        pixmap = self.fetchItemPixmap(gameData[PUUID]['item4'])
        label.setPixmap(pixmap)
        items.addWidget(label, 1, 1)
        
        label = QLabel()
        pixmap = self.fetchItemPixmap(gameData[PUUID]['item5'])
        label.setPixmap(pixmap)
        items.addWidget(label, 1, 2)
        
        itemBox.setLayout(items)
        boxLayout.addWidget(itemBox, 0, 3, -1, 1)
        
        
        champBox = QGroupBox()
        champs = QGridLayout()
        
        for i, player in enumerate(list(gameData.keys())):
            label = QLabel()
            pixmap = self.fetchChampPixmap(gameData[player]['champion_name'])
            label.setPixmap(pixmap)
            if i < 5:
                champs.addWidget(label, 0, i)
            else:
                champs.addWidget(label, 1, i - 5)
        
        champBox.setLayout(champs)
        boxLayout.addWidget(champBox, 0, 4, -1, 1)
        
        
        box.setLayout(boxLayout)
        layout.addWidget(box)
        self.setLayout(layout)
    
    
    def fetchItemPixmap(self, itemID):
        if itemID == 0:
            pixmap = QPixmap(30, 30)
            pixmap.fill(QColor(100, 100, 100))
            return pixmap
        
        pixmap = QPixmap(self.IMAGE_LOCATION + 'item/' + str(itemID) + '.png').scaled(30, 30, mode=Qt.SmoothTransformation)
        
        return pixmap
    
    
    def fetchChampPixmap(self, champName):
        pixmap = QPixmap(self.IMAGE_LOCATION + 'champion/' + str(champName) + '.png').scaled(30, 30, mode=Qt.SmoothTransformation)

        return pixmap