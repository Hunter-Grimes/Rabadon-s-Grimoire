from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QHBoxLayout, QGraphicsOpacityEffect
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt

import json

import asyncio
from asyncWorker import Worker
from callLocalRiotAPI import setRunes

class RuneSelector(QWidget):
    def __init__(self, DATA_LOCATION, suggestions, champName, threadPool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.primaryTree = suggestions['primaryStyleID']
        self.secondaryTree = suggestions['subStyleID']
        self.champName = champName
        self.threadPool = threadPool
        
        pipInfo = None
        primaryTreeData = None
        secondaryTreeData = None
        
        self.primaryTreeSelections = {}
        self.secondaryTreeSelections = [(None, None), (None, None)]
        self.pips = {}
        self.secondaryTreeIndex = 0
        
        with open(DATA_LOCATION + 'data/en_US/runesReforged.json') as runeInfo:
            info = json.load(runeInfo)
            for rune in info:
                if rune['id'] == self.primaryTree:
                    primaryTreeData = rune
                if rune['id'] == self.secondaryTree:
                    secondaryTreeData = rune
                    
        with open('exeFrontend/pipInfo.json', 'r') as pips:
            pipInfo = json.load(pips)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        #Primary Tree
        keyStone = runeOptions(primaryTreeData['slots'][0]['runes'], suggestions, self, 'keyStone')
        layout.addWidget(keyStone, 0, 0, 1, 1, Qt.AlignCenter)
        keyStone.changeRune(suggestions['primaryStyle1'])
        
        primary1 = runeOptions(primaryTreeData['slots'][1]['runes'], suggestions, self, 'primary1')
        layout.addWidget(primary1, 1, 0, 1, 1, Qt.AlignCenter)
        primary1.changeRune(suggestions['primaryStyle2'])
        
        primary2 = runeOptions(primaryTreeData['slots'][2]['runes'], suggestions, self, 'primary2')
        layout.addWidget(primary2, 2, 0, 1, 1, Qt.AlignCenter)
        primary2.changeRune(suggestions['primaryStyle3'])
        
        primary3 = runeOptions(primaryTreeData['slots'][3]['runes'], suggestions, self, 'primary3')
        layout.addWidget(primary3, 3, 0, 1, 1, Qt.AlignCenter)
        primary3.changeRune(suggestions['primaryStyle4'])
        
        #Secondary Tree
        secondary1 = runeOptions(secondaryTreeData['slots'][1]['runes'], suggestions, self, 'secondary1')
        layout.addWidget(secondary1, 0, 1, 1, 1, Qt.AlignCenter)
        secondary1.changeRune(suggestions['subStyle1'])
        secondary1.changeRune(suggestions['subStyle2'])
        
        secondary2 = runeOptions(secondaryTreeData['slots'][2]['runes'], suggestions, self, 'secondary2')
        layout.addWidget(secondary2, 1, 1, 1, 1, Qt.AlignCenter)
        secondary2.changeRune(suggestions['subStyle1'])
        secondary2.changeRune(suggestions['subStyle2'])
        
        secondary3 = runeOptions(secondaryTreeData['slots'][3]['runes'], suggestions, self, 'secondary3')
        layout.addWidget(secondary3, 2, 1, 1, 1, Qt.AlignCenter)
        secondary3.changeRune(suggestions['subStyle1'])
        secondary3.changeRune(suggestions['subStyle2'])
        
        #Pips
        pip1 = runeOptions(pipInfo['offense'], suggestions, self, 'pip1')
        layout.addWidget(pip1, 3, 1, 1, 1, Qt.AlignCenter)
        pip1.changeRune(suggestions['offensePerk'])
        
        pip2 = runeOptions(pipInfo['flex'], suggestions, self, 'pip2')
        layout.addWidget(pip2, 4, 1, 1, 1, Qt.AlignCenter)
        pip2.changeRune(suggestions['flexPerk'])
        
        pip3 = runeOptions(pipInfo['defense'], suggestions, self, 'pip3')
        layout.addWidget(pip3, 5, 1, 1, 1, Qt.AlignCenter)
        pip3.changeRune(suggestions['defensePerk'])
        
        #Export
        push = QPushButton('Push to LOL')
        push.clicked.connect(self.pushToLol)
        layout.addWidget(push, 6, 0, 1, 2, Qt.AlignCenter)
        
        
        
        self.setLayout(layout)

    def optionChosen(self, id, optionType, controller):
        if 'secondary' not in optionType:
            if 'pip' in optionType:
                self.pips[optionType] = id
            else:
                self.primaryTreeSelections[optionType] = id
        else:
            for i, data in enumerate(self.secondaryTreeSelections):
                if data[1] == controller:
                    self.secondaryTreeSelections[i] = (id, controller)
                    if i == 1:
                        self.secondaryTreeIndex = 0
                    else:
                        self.secondaryTreeIndex = 1
                    return
            match self.secondaryTreeIndex:
                case 0:
                    if self.secondaryTreeSelections[0][0] is not None:
                        self.secondaryTreeSelections[0][1].changeRune(None)
                    self.secondaryTreeSelections[0] = (id, controller)
                    self.secondaryTreeIndex = 1
                    
                case 1:
                    if self.secondaryTreeSelections[1][0] is not None:
                        self.secondaryTreeSelections[1][1].changeRune(None)
                    self.secondaryTreeSelections[1] = (id, controller)
                    self.secondaryTreeIndex = 0

    def pushToLol(self):
        runeIDs = [val for val in list(self.primaryTreeSelections.values())] + [x[0] for x in self.secondaryTreeSelections] + [x for x in list(self.pips.values())]
        reqBody = {
            "name": "Rabadon's Grimoire - " + self.champName,
            "primaryStyleId": self.primaryTree,
            "subStyleId": self.secondaryTree,
            "selectedPerkIds": runeIDs,
            "current": True
        }
        worker = Worker(lambda: asyncio.run(setRunes(reqBody)))
        self.threadPool.start(worker)


class runeOptions(QWidget):
    def __init__(self, options, suggestions, runeSelector, optionType, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.runeSelector = runeSelector
        IMAGE_LOCATION = 'dragontailData/img/'
        
        self.optionType = optionType
        
        layout = QHBoxLayout()
        
        for option in options:
            button = runeButton(option, suggestions, IMAGE_LOCATION, self, self.runeSelector)
            layout.addWidget(button)
        
        self.setLayout(layout)
    
    def changeRune(self, id):
        if id is None:
            for button in [self.layout().itemAt(x).widget() for x in range(self.layout().count())]:
                button.unchecked()
            return
        
        if id not in [self.layout().itemAt(x).widget().id for x in range(self.layout().count())]:
            return

        for button in [self.layout().itemAt(x).widget() for x in range(self.layout().count())]:
            if button.id == id:
                button.checked()
                self.runeSelector.optionChosen(id, self.optionType, self)
            else:
                button.unchecked()


class runeButton(QPushButton):
    def __init__(self, info, suggestions, IMAGE_LOCATION, runeOptions, runeSelector, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = info['id']
        self.runeOptions = runeOptions
        self.runeSelector = runeSelector
        
        icon = QIcon()

        self.pixmap = QPixmap(IMAGE_LOCATION + info['icon'])
        self.pixmap = self.pixmap.scaled(25, 25, mode=Qt.SmoothTransformation)
        icon.addPixmap(self.pixmap)
        self.setIcon(icon)
        
        self.setIconSize(self.pixmap.size())
        self.setFixedSize(self.pixmap.size().width(), self.pixmap.size().height())
        self.setStyleSheet("border-radius: " + str(self.pixmap.size().width() / 2) + "px;")

        self.setToolTip(info['name'])
        
        self.unchecked()
        
        self.clicked.connect(lambda: self.runeOptions.changeRune(self.id))
        
    def checked(self):
        effect = QGraphicsOpacityEffect(self)
        effect.setOpacity(1)
        self.setGraphicsEffect(effect)
        
    def unchecked(self):
        effect = QGraphicsOpacityEffect(self)
        effect.setOpacity(0.2)
        self.setGraphicsEffect(effect)