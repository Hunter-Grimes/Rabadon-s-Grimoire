from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
import requests
from asyncWorker import Worker

class userTagsDisplay(QWidget):
    def __init__(self, PUUID, BASE_URL, threadpool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threadPool = threadpool
        self.PUUID = PUUID
        self.BASE_URL = BASE_URL
        
        layout = QHBoxLayout()
        layout.setSpacing(5)
        self.setLayout(layout)
        
        worker = Worker(self.fetchTags)
        worker.signals.result.connect(self.displayTags)
        
        self.threadPool.start(worker)
        
    def fetchTags(self):
        tags = requests.get(self.BASE_URL + '/user/tags/' + self.PUUID).json()
        
        return tags
    
    def displayTags(self, tags):
        for tag in tags.keys():
            if 'lover' in tag:
                self.loverTag(tag, tags[tag])
            
    def loverTag(self, champ, numGames):
        loverTag = QLabel(champ)
        loverTag.setToolTip("This player has played " + str(numGames) + " games of " + (champ.removesuffix(" lover")))
        loverTag.setAlignment(Qt.AlignCenter)
        loverTag.setFixedHeight(25)
        loverTag.setFixedWidth(100)
        loverTag.setStyleSheet("background-color: transparent; color: green; border: 2px solid green; border-radius: 10px;")
        self.layout().addWidget(loverTag)