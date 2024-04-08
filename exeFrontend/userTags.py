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
            self.tag(tag, tags[tag])
    
    def tag(self, champ, info):
        tag = QLabel(champ)
        tag.setToolTip(info[1])
        tag.setAlignment(Qt.AlignCenter)
        tag.setFixedHeight(25)
        tag.setFixedWidth(100)
        
        match info[0]:
            case 0:
                tag.setStyleSheet("background-color: transparent; color: green; border: 2px solid green; border-radius: 10px;")
            case 1:
                tag.setStyleSheet("background-color: transparent; color: red; border: 2px solid red; border-radius: 10px;")
            case 2:
                tag.setStyleSheet("background-color: transparent; color: gray; border: 2px solid gray; border-radius: 10px;")
            case _:
                pass
            
        self.layout().addWidget(tag)