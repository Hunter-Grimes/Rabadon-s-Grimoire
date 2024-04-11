from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea, QGroupBox, QPushButton, QProgressBar
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import Qt


class championStatsHandler(QWidget):
    def __init__(self, PUUID, totalGames, champStats, manager, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.championStats = championStats(PUUID, totalGames, champStats, manager, IMAGE_LOCATION)
        layout = QGridLayout()
        layout.setContentsMargins(1, 2, 1, 2)
        layout.setVerticalSpacing(5)
        
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
        self.setFixedWidth(self.championStats.width())
        
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
    def __init__(self, PUUID, totalGames, champStats, manager, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.totalGames = totalGames
        self.champStats = champStats
        self.manager = manager
        self.threadPool = manager.threadPool
        self.IMAGE_LOCATION = IMAGE_LOCATION
        
        group = QGroupBox()
        
        boxlayout = QVBoxLayout()
        for champ in champStats.keys():
            boxlayout.addWidget(champStatsChip(PUUID, self.totalGames, champ, self.champStats[champ], self.manager, self.IMAGE_LOCATION))

        group.setLayout(boxlayout)
        self.setWidget(group)
        self.setFixedWidth(group.width() + 2)
        self.setWidgetResizable(True)
        


class champStatsChip(QWidget):
    def __init__(self, PUUID, totalGames, championName, stats, manager, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.myFont = QFont()
        self.myFont.setPointSize(10)
        
        self.PUUID = PUUID
        
        self.totalGames = totalGames
        
        self.championName = championName
        self.champGamesPlayed = stats['gamesPlayed']
        self.winPercentage = stats['wins'] / stats['gamesPlayed']
        
        self.stats = stats
        self.manager = manager
        self.IMAGE_LOCATION = IMAGE_LOCATION
        
        layout = QVBoxLayout()
        layout.setContentsMargins(1, 1, 1, 1)
        
        box = QGroupBox()
        box.setFixedSize(300, 85)
        boxLayout = QGridLayout()
        
        #Champion Icon
        champButton = QPushButton()
        champButton.setStyleSheet("QPushButton { background: rgba(0, 0, 0, 0.5); border-radius: 5px; } QPushButton:Pressed { background-color: rgb(255,255,255);}")
        pixmap = QPixmap(self.IMAGE_LOCATION + 'champion/' + self.championName + '.png')
        pixmap = pixmap.scaled(40, 40, mode=Qt.SmoothTransformation)
        icon = QIcon()
        
        icon.addPixmap(pixmap)
        champButton.setIcon(icon)
        
        champButton.setIconSize(pixmap.size())
        champButton.setFixedSize(pixmap.size())
        
        boxLayout.addWidget(champButton, 0, 0, 4, 1, alignment=Qt.AlignCenter)
        
        champButton.pressed.connect(lambda: self.manager.createChampStatsPage(self.PUUID, self.championName))
        
        #Champion Name
        label = QLabel(self.championName)
        label.setFont(self.myFont)
        label.setAlignment(Qt.AlignCenter)
        boxLayout.addWidget(label, 1, 1, 1, 1, alignment=Qt.AlignCenter)
        
        #KDA
        kda = str(self.stats['avgKill']) + '/' + str(self.stats['avgDeath']) + '/' + str(self.stats['avgAssist'])
        label = QLabel(kda)
        label.setFont(self.myFont)
        label.setAlignment(Qt.AlignCenter)
        boxLayout.addWidget(label, 2, 1, 1, 1, alignment=Qt.AlignCenter)
        
        #Games Played
        gamesPlayed = QProgressBar()
        gamesPlayed.setMaximum(self.totalGames)
        gamesPlayed.setValue(self.stats['gamesPlayed'])
        boxLayout.addWidget(gamesPlayed, 1, 2, 1, 1, alignment=Qt.AlignCenter)
        
        numGamesPlayed = QLabel(str(self.stats['gamesPlayed']))
        numGamesPlayed.setFont(self.myFont)
        numGamesPlayed.setAlignment(Qt.AlignCenter)
        boxLayout.addWidget(numGamesPlayed, 2, 2, 1, 1, alignment=Qt.AlignCenter)
        
        #Games Won
        gamesWon = QProgressBar()
        gamesWon.setMaximum(self.stats['gamesPlayed'])
        gamesWon.setValue(self.stats['wins'])
        boxLayout.addWidget(gamesWon, 1, 3, 1, 1, alignment=Qt.AlignCenter)
        
        numGamesWon = QLabel(str(round((self.stats['wins'] / self.stats['gamesPlayed']) * 100, 2)) + '%')
        numGamesWon.setFont(self.myFont)
        numGamesWon.setAlignment(Qt.AlignCenter)
        boxLayout.addWidget(numGamesWon, 2, 3, 1, 1, alignment=Qt.AlignCenter)
        
        box.setLayout(boxLayout)
        layout.addWidget(box)
        self.setLayout(layout)
        
        