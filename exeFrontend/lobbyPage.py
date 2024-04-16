from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QGroupBox, QHBoxLayout

from runeSuggestion import RuneSelector
from callLocalRiotAPI import champSelectWorker
from fetchData import fetchRuneRecommendation
from asyncWorker import Worker

class LobbyPage(QWidget):
    def __init__(self, threadPool, summoner, BASE_URL, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.BASE_URL = BASE_URL
        self.threadPool = threadPool
        self.summoner = summoner
        
        layout = QGridLayout()
        layout.addWidget(QLabel("Lobby In Progress"))
        
        self.runeSelectorBox = QGroupBox()
        self.boxLayout = QHBoxLayout()
        self.boxLayout.setContentsMargins(0, 0, 0, 0)
        self.runeSelectorBox.setContentsMargins(0, 0, 0, 0)
        
        self.runesWidget = QWidget()
        
        self.boxLayout.addWidget(self.runesWidget)
        self.runeSelectorBox.setLayout(self.boxLayout)
        self.runeSelectorBox.setMaximumSize(275, 350)

        layout.addWidget(self.runeSelectorBox, 0, 1)
        
        champSelectHover = champSelectWorker(self.summoner['puuid'])
        champSelectHover.signals.progress.connect(lambda CID: self.champSelected('don\'t have name', CID))
        self.threadPool.start(champSelectHover)
        
        self.setLayout(layout)
        
    def champSelected(self, champName, CID):
        worker = Worker(fetchRuneRecommendation, CID, self.BASE_URL)
        worker.signals.result.connect(lambda info: self.changeRuneRecommendations(champName, info))
        self.threadPool.start(worker)
        
    def changeRuneRecommendations(self, champName, info):
        newRunes = RuneSelector('dragontailData/14.5.1/', info, champName, self.threadPool)
        self.boxLayout.replaceWidget(self.runesWidget, newRunes)
        self.runeSelectorBox.update()
        self.runesWidget = newRunes