from collections import defaultdict

from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QGroupBox, QHBoxLayout, QVBoxLayout, QProgressBar
from PySide6.QtCore import Qt

from dataFiles import find_data_file
from runeSuggestion import RuneSelector
from callLocalRiotAPI import champSelectWorker
from fetchData import(
    fetchRuneRecommendation, fetchChampPixmap, fetchRolePixmap, fetchChampSelectInfoGeneric,
    fetchChampSelectInfoSpecific, fetchChampSpecificTags
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
        self.champSelectArray = champSelectChipArrayLobby(self.summoner['puuid'], self.BASE_URL, self.threadPool)
        layout.addWidget(self.champSelectArray, 0, 0, 2, 1)
        
        self.runeSelectorBox = QGroupBox()
        self.boxLayout = QVBoxLayout()
        self.boxLayout.addWidget(QLabel("Rune Suggestions"), alignment=Qt.AlignCenter)
        self.boxLayout.setContentsMargins(0, 0, 0, 0)
        self.runeSelectorBox.setContentsMargins(0, 0, 0, 0)
        
        self.runesWidget = QWidget()
        
        self.boxLayout.addWidget(self.runesWidget)
        self.runeSelectorBox.setLayout(self.boxLayout)
        self.runeSelectorBox.setFixedSize(275, 350)

        layout.addWidget(self.runeSelectorBox, 0, 1)
        
        self.damageIndicator = damageIndicator()
        layout.addWidget(self.damageIndicator, 1, 1)
        
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
        worker.signals.result.connect(lambda info: self.updateDamageIndicator(info))
        self.threadPool.start(worker)
        
    def champSelected(self, CID):
        worker = Worker(fetchRuneRecommendation, CID, self.BASE_URL)
        worker.signals.result.connect(lambda info: self.changeRuneRecommendations(info))
        self.threadPool.start(worker)
        
    def changeRuneRecommendations(self, info):
        IMAGE_LOCATION = 'dragontailData/14.5.1/'
        IMAGE_LOCATION = find_data_file(IMAGE_LOCATION)
        
        newRunes = RuneSelector(IMAGE_LOCATION, info, info['champName'], self.threadPool)
        self.boxLayout.removeWidget(self.runesWidget)
        self.runesWidget.deleteLater()
        self.boxLayout.addWidget(newRunes)
        self.runesWidget = newRunes
        self.runeSelectorBox.update()
        self.boxLayout.update()

    def getChipInfo(self, toUpdate):
        for i, player in enumerate(toUpdate['myTeam']):
            if player['puuid'] == self.summoner['puuid']:
                info = fetchChampSelectInfoSpecific(player['championId'], self.summoner['gameName'], self.summoner['tagLine'], self.BASE_URL)
                info['role'] = player['assignedPosition']
                if player['assignedPosition'] not in ["TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"]:
                    info['role'] = player['cellId']
                toUpdate['myTeam'][i] = (player, info)
            else:
                info = fetchChampSelectInfoGeneric(player['championId'], self.BASE_URL)
                info['role'] = player['assignedPosition']
                if player['assignedPosition'] not in ["TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"]:
                    info['role'] = player['cellId']
                toUpdate['myTeam'][i] = (player, info)
                
        for i, player in enumerate(toUpdate['theirTeam']):
            info = fetchChampSelectInfoGeneric(player['championId'], self.BASE_URL)
            info['role'] = player['assignedPosition']
            if player['assignedPosition'] not in ["TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"]:
                    info['role'] = player['cellId']
            toUpdate['theirTeam'][i] = (player, info)
            
        return toUpdate
    
    def updateDamageIndicator(self, info):
        self.damageIndicator.updateDamageIndicator(info)

       
class damageIndicator(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.totalDamage = defaultdict(lambda: 0)
        self.damageIndicator = None
        self.layout = QHBoxLayout()
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.box = QGroupBox()
        self.boxLayout = QVBoxLayout()
        self.boxLayout.addWidget(QLabel('Your Team\'s Damage Spread'), alignment=Qt.AlignCenter)
        self.box.setFixedSize(275, 100)
        self.box.setLayout(self.boxLayout)
        
        self.layout.addWidget(self.box)

        self.setLayout(self.layout)

    def updateDamageIndicator(self, info):
        for player in info['myTeam']:
            self.totalDamage[player[0]['summonerId']] = (player[1]['averageMagicDamage'], player[1]['averagePhysicalDamage'], player[1]['averageTrueDamage'])
        
        totalMagic = sum([x[0] for x in self.totalDamage.values()])
        totalPhysical = sum([x[1] for x in self.totalDamage.values()])
        totalTrue = sum([x[2] for x in self.totalDamage.values()])

        if totalMagic + totalPhysical + totalTrue == 0:
            return
        
        if self.damageIndicator is not None:
            newDamage = damageBar(totalMagic, totalPhysical, totalTrue)
            self.boxLayout.replaceWidget(self.damageIndicator, newDamage)
            self.damageIndicator = newDamage
        else:
            newDamage = damageBar(totalMagic, totalPhysical, totalTrue)
            self.boxLayout.addWidget(newDamage)
            self.damageIndicator = newDamage 

        self.box.update()


class damageBar(QProgressBar):
    def __init__(self, totalMagic, totalPhysical, totalTrue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        totalDamage = float(totalMagic) + float(totalPhysical) + float(totalTrue)
        percentMagic = totalMagic / totalDamage
        percentPhysical = totalPhysical / totalDamage
        
        self.setFixedSize(250, 20)
        self.setOrientation(Qt.Horizontal)
        self.setStyleSheet(
            "::chunk {"
            "background-color: qlineargradient(x0: 0, x2: 1, "
            "stop: 0 blue, stop: " + str(percentMagic) + " blue, "
            "stop: " + str(percentMagic) + " red, stop: " + str(percentMagic + percentPhysical) + " red, "
            "stop: " + str(percentMagic + percentPhysical) + " gray, stop: 1 gray)"
            "}"
        )
        self.setValue(100)
        self.setAlignment(Qt.AlignCenter)
        self.setTextVisible(False)


class champSelectChipArrayLobby(QWidget):
    def __init__(self, myPUUID, BASE_URL, threadPool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.puuid = myPUUID
        self.BASE_URL = BASE_URL
        self.threadPool = threadPool

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
                chip = specificChampSelectChip(player[1], player[0]['championId'], self.BASE_URL, self.threadPool)
            else:
                chip = genericChampSelectChip(player[1])
                
            match player[0]['assignedPosition']:
                
                case 'TOP':
                    oldWidget = self.layout.itemAtPosition(0, 0).widget()
                    self.layout.replaceWidget(oldWidget, chip)
                    oldWidget.deleteLater()
                case 'JUNGLE':
                    oldWidget = self.layout.itemAtPosition(0, 1).widget()
                    self.layout.replaceWidget(oldWidget, chip)
                    oldWidget.deleteLater()

                case 'MIDDLE':
                    oldWidget = self.layout.itemAtPosition(0, 2).widget()
                    self.layout.replaceWidget(oldWidget, chip)
                    oldWidget.deleteLater()

                case 'BOTTOM':
                    oldWidget = self.layout.itemAtPosition(0, 3).widget()
                    self.layout.replaceWidget(oldWidget, chip)
                    oldWidget.deleteLater()

                case 'UTILITY':
                    oldWidget = self.layout.itemAtPosition(0, 4).widget()
                    self.layout.replaceWidget(oldWidget, chip)
                    oldWidget.deleteLater()
                    
                case _:
                    oldWidget = self.layout.itemAtPosition(0, int(player[1]['role']) % 4).widget()
                    self.layout.replaceWidget(oldWidget, chip)
                    oldWidget.deleteLater()
        
        for player in info['theirTeam']:
            if player[0]['championId'] == 0:
                continue
            
            chip = genericChampSelectChip(player[1])
            
            match player[0]['assignedPosition']:

                case 'TOP':
                    oldWidget = self.layout.itemAtPosition(1, 0).widget()
                    self.layout.replaceWidget(oldWidget, chip)
                    oldWidget.deleteLater()

                case 'JUNGLE':
                    oldWidget = self.layout.itemAtPosition(1, 1).widget()
                    self.layout.replaceWidget(oldWidget, chip)
                    oldWidget.deleteLater()

                case 'MIDDLE':
                    oldWidget = self.layout.itemAtPosition(1, 2).widget()
                    self.layout.replaceWidget(oldWidget, chip)
                    oldWidget.deleteLater()

                case 'BOTTOM':
                    oldWidget = self.layout.itemAtPosition(1, 3).widget()
                    self.layout.replaceWidget(oldWidget, chip)
                    oldWidget.deleteLater()

                case 'UTILITY':
                    oldWidget = self.layout.itemAtPosition(1, 4).widget()
                    self.layout.replaceWidget(oldWidget, chip)
                    oldWidget.deleteLater()
                
                case _:
                    oldWidget = self.layout.itemAtPosition(1, int(player[1]['role']) % 4).widget()
                    self.layout.replaceWidget(oldWidget, chip)
                    oldWidget.deleteLater()
                    
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
        self.IMAGE_LOCATION = find_data_file(self.IMAGE_LOCATION)
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
        
        if self.info['role'] not in ["TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"]:
            roleName = QLabel("None")
            roleName.setAlignment(Qt.AlignCenter)
            self.boxLayout.addWidget(roleName)
        else:
            roleName = QLabel(self.info['role'])
            roleName.setAlignment(Qt.AlignCenter)
            self.boxLayout.addWidget(roleName)

    def setLabel(self):
        name = QLabel(self.info['champName'])
        name.setAlignment(Qt.AlignCenter)
        self.boxLayout.addWidget(name)

    
class specificChampSelectChip(genericChampSelectChip):
    def __init__(self, info, CID, BASE_URL, threadPool, *args, **kwargs):
        super().__init__(info, *args, **kwargs)
        self.info = info
        self.CID = CID
        self.BASE_URL = BASE_URL
        self.threadPool = threadPool
        
        self.getTags()
        
    def setLabel(self):
        name = QLabel(self.info['gameName'] + " #" + self.info['tagLine'])
        name.setAlignment(Qt.AlignCenter)
        self.boxLayout.addWidget(name)
        
    def getTags(self):
        worker = Worker(fetchChampSpecificTags, self.CID, self.info['gameName'], self.info['tagLine'], self.info['role'], self.BASE_URL)
        worker.signals.result.connect(self.addTags)
        self.threadPool.start(worker)
    
    def addTags(self, info):
        self.boxLayout.addWidget(champSelectTagDisplay(info))
        self.update()

       
class champSelectTagDisplay(QWidget):
    def __init__(self, info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.numTags = 0
        
        layout = QGridLayout()
        layout.setSpacing(10)
        self.setLayout(layout)
        
        self.displayTags(info)
    
    def displayTags(self, tags):
        for tag in tags.keys():
            self.tag(tag, tags[tag])
    
    def tag(self, champ, info):
        tag = QLabel(champ)
        tag.setToolTip(info[1])
        tag.setAlignment(Qt.AlignCenter)
        tag.setFixedHeight(15)
        tag.setFixedWidth(75)
        
        match info[0]:
            case 0:
                tag.setStyleSheet("background-color: transparent; color: green; border: 2px solid green; border-radius: 5px; font-size: 10px;")
            case 1:
                tag.setStyleSheet("background-color: transparent; color: red; border: 2px solid red; border-radius: 5px; font-size: 10px;")
            case 2:
                tag.setStyleSheet("background-color: transparent; color: gray; border: 2px solid gray; border-radius: 5px; font-size: 10px;")
            case _:
                pass
        
        self.layout().addWidget(tag, (self.numTags // 2), (self.numTags % 2))
        self.numTags += 1