from collections import defaultdict

from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QGroupBox, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt

from runeSuggestion import RuneSelector
from callLocalRiotAPI import champSelectWorker
from fetchData import(
    fetchRuneRecommendation, fetchChampPixmap, fetchRolePixmap, fetchChampSelectInfoGeneric,
    fetchChampSelectInfoSpecific
)
from asyncWorker import Worker


class LobbyPage(QWidget):
    def __init__(self, threadPool, summoner, BASE_URL, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.BASE_URL = BASE_URL
        self.threadPool = threadPool
        self.summoner = summoner
        self.selectedChamps = defaultdict(lambda: 0)
        
        layout = QGridLayout()
        self.champSelectArray = champSelectChipArrayLobby(self.summoner['puuid'])
        layout.addWidget(self.champSelectArray, 0, 0)
        
        self.runeSelectorBox = QGroupBox()
        self.boxLayout = QHBoxLayout()
        self.boxLayout.setContentsMargins(0, 0, 0, 0)
        self.runeSelectorBox.setContentsMargins(0, 0, 0, 0)
        
        self.runesWidget = QWidget()
        
        self.boxLayout.addWidget(self.runesWidget)
        self.runeSelectorBox.setLayout(self.boxLayout)
        self.runeSelectorBox.setFixedSize(275, 350)

        layout.addWidget(self.runeSelectorBox, 0, 1)
        
        champSelectHover = champSelectWorker(self.summoner['puuid'])
        champSelectHover.signals.progress.connect(self.parseLobbyData)
        self.threadPool.start(champSelectHover)
        
        self.setLayout(layout)
        
    def parseLobbyData(self, data):
        toUpdate = {
            'myTeam': [],
            'theirTeam': []
        }
        for player in data['myTeam']:
            if self.selectedChamps[player['summonerId']] == player['championId'] or player['championId'] == 0:
                continue
            
            self.selectedChamps[player['summonerId']] = player['championId']
            
            if player['puuid'] == self.summoner['puuid']:
                self.champSelected(player['championId'])
                
            toUpdate['myTeam'].append(player)
        
        for player in data['theirTeam']:
            if self.selectedChamps[player['summonerId']] == player['championId'] or player['championId'] == 0:
                continue
            
            self.selectedChamps[player['summonerId']] = player['championId']
                
            toUpdate['theirTeam'].append(player)
        
        worker = Worker(self.getChipInfo, toUpdate)
        worker.signals.result.connect(lambda info: self.champSelectArray.updateChampSelect(info))
        self.threadPool.start(worker)
        
    def champSelected(self, CID):
        worker = Worker(fetchRuneRecommendation, CID, self.BASE_URL)
        worker.signals.result.connect(lambda info: self.changeRuneRecommendations(info))
        self.threadPool.start(worker)
        
    def changeRuneRecommendations(self, info):
        newRunes = RuneSelector('dragontailData/14.5.1/', info, info['champName'], self.threadPool)
        self.boxLayout.replaceWidget(self.runesWidget, newRunes)
        self.runeSelectorBox.update()
        self.runesWidget = newRunes

    def getChipInfo(self, toUpdate):
        for i, player in enumerate(toUpdate['myTeam']):
            if player['puuid'] == self.summoner['puuid']:
                info = fetchChampSelectInfoSpecific(player['championId'], self.summoner['gameName'], self.summoner['tagLine'], self.BASE_URL)
                info['role'] = player['assignedPosition']
                toUpdate['myTeam'][i] = (player, info)
            else:
                info = fetchChampSelectInfoGeneric(player['championId'], self.BASE_URL)
                info['role'] = player['assignedPosition']
                toUpdate['myTeam'][i] = (player, info)
                
        for i, player in enumerate(toUpdate['theirTeam']):
            info = fetchChampSelectInfoGeneric(player['championId'], self.BASE_URL)
            info['role'] = player['assignedPosition']
            toUpdate['theirTeam'][i] = (player, info)
            
        return toUpdate


class champSelectChipArrayLobby(QWidget):
    def __init__(self, myPUUID, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.puuid = myPUUID

        self.layout = QGridLayout()
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        
        for row in range(2):
            for i in range(5):
                self.layout.addWidget(champSelectChipTemplate(), row, i)

        self.setLayout(self.layout)
        
    def updateChampSelect(self, info):
        for player in info['myTeam']:
            if player[0]['championId'] == 0:
                continue
            
            if player[0]['puuid'] == self.puuid:
                chip = specificChampSelectChip(player[1])
            else:
                chip = genericChampSelectChip(player[1])
                
            match player[0]['assignedPosition']:
                
                case 'TOP':
                    self.layout.replaceWidget(self.layout.itemAtPosition(0, 0).widget(), chip)

                case 'JUNGLE':
                    self.layout.replaceWidget(self.layout.itemAtPosition(0, 1).widget(), chip)

                case 'MIDDLE':
                    self.layout.replaceWidget(self.layout.itemAtPosition(0, 2).widget(), chip)

                case 'BOTTOM':
                    self.layout.replaceWidget(self.layout.itemAtPosition(0, 3).widget(), chip)

                case 'UTILITY':
                    self.layout.replaceWidget(self.layout.itemAtPosition(0, 4).widget(), chip)
                    
                case _:
                    self.layout.replaceWidget(self.layout.itemAtPosition(0, 2).widget(), chip)
        
        for player in info['theirTeam']:
            if player[0]['championId'] == 0:
                continue
            
            chip = genericChampSelectChip(player[1])
            
            match player[0]['assignedPosition']:

                case 'TOP':
                    self.layout.replaceWidget(self.layout.itemAtPosition(1, 0).widget(), chip)

                case 'JUNGLE':
                    self.layout.replaceWidget(self.layout.itemAtPosition(1, 1).widget(), chip)

                case 'MIDDLE':
                    self.layout.replaceWidget(self.layout.itemAtPosition(1, 2).widget(), chip)

                case 'BOTTOM':
                    self.layout.replaceWidget(self.layout.itemAtPosition(1, 3).widget(), chip)

                case 'UTILITY':
                    self.layout.replaceWidget(self.layout.itemAtPosition(1, 4).widget(), chip)
                    
        self.update()


class champSelectChipTemplate(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.box = QGroupBox()
        self.boxLayout = QVBoxLayout()
        self.box.setFixedSize(175, 250)
        self.box.setLayout(self.boxLayout)
        
        self.box.setContentsMargins(0, 0, 0, 0)
        self.boxLayout.setContentsMargins(0, 0, 0, 0)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.box)
        
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(self.layout)

       
class genericChampSelectChip(champSelectChipTemplate):
    def __init__(self, info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.IMAGE_LOCATION = 'dragontailData/14.5.1/img/'
        self.info = info
        
        self.setLabel()
        
        champIcon = QLabel()
        champPixmap = fetchChampPixmap(self.info['champName'], self.IMAGE_LOCATION)
        champIcon.setPixmap(champPixmap)
        champIcon.setAlignment(Qt.AlignCenter)
        self.boxLayout.addWidget(champIcon)
        
        winPercent = QLabel(f"{str(round(self.info['winPercent'] * 100, 2))}%")
        winPercent.setAlignment(Qt.AlignCenter)
        self.boxLayout.addWidget(winPercent)
        
        role = QLabel()
        rolePixmap = fetchRolePixmap(self.info['role'])
        role.setPixmap(rolePixmap)
        role.setAlignment(Qt.AlignCenter)
        self.boxLayout.addWidget(role)
        
        roleName = QLabel(self.info['role'])
        roleName.setAlignment(Qt.AlignCenter)
        self.boxLayout.addWidget(roleName)

    def setLabel(self):
        name = QLabel(self.info['champName'])
        name.setAlignment(Qt.AlignCenter)
        self.boxLayout.addWidget(name)

    
class specificChampSelectChip(genericChampSelectChip):
    def __init__(self, info, *args, **kwargs):
        super().__init__(info, *args, **kwargs)
        self.info = info
        
    def setLabel(self):
        name = QLabel(self.info['gameName'] + " #" + self.info['tagLine'])
        name.setAlignment(Qt.AlignCenter)
        self.boxLayout.addWidget(name)