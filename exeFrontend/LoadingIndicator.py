from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QMovie

from dataFiles import find_data_file

class LoadingIndicator(QLabel):
    def __init__(self, manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        
        self.setFixedSize(20, 20)
        loadingLocation = find_data_file('loading.gif')
        
        self.movie = QMovie(loadingLocation)
        self.movie.setScaledSize(self.size())
        self.setMovie(self.movie)
        
    def startAnimation(self):
        self.show()
        self.movie.start()
        
    def stopAnimation(self):
        if (not self.manager.fetchingPlayer) and (not self.manager.fetchingGames):
            self.movie.stop()
            self.hide()