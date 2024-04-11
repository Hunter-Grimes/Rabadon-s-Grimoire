from PySide6.QtWidgets import QWidget, QGridLayout

from matchHistory import champMatchHistory

class ChampStatsPageManager(QWidget):
    def __init__(self, info, manager, BASE_URL, threadpool, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.threadPool = threadpool
        
        self.BASE_URL = BASE_URL
        self.IMAGE_LOCATION = IMAGE_LOCATION
        
        self.layout = QGridLayout()
        
        ChampionPage(info, self.manager, IMAGE_LOCATION)
        
        self.layout.addWidget(ChampionPage(info, self.manager, IMAGE_LOCATION), 0, 0)
        
        self.setLayout(self.layout)


class ChampionPage(QWidget):
    def __init__(self, info, manager, IMAGE_LOCATION, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.info = info
        self.manager = manager
        self.threadPool = self.manager.threadPool
        self.IMAGE_LOCATION = IMAGE_LOCATION
        
        self.gameIDs = info['gameData']

        layout = QGridLayout()
        
        #Match History
        history = champMatchHistory(info, self.manager, IMAGE_LOCATION)
        layout.addWidget(history, 0, 0, 1, 2)
        
        self.setLayout(layout)