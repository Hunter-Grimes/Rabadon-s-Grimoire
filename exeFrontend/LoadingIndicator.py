from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QMovie

class LoadingIndicator(QLabel):
    def __init__(self, manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        
        self.setFixedSize(20, 20)
        self.movie = QMovie('exeFrontend/loading.gif')
        self.movie.setScaledSize(self.size())
        self.setMovie(self.movie)
        
    def startAnimation(self):
        self.show()
        self.movie.start()
        
    def stopAnimation(self):
        if (not self.manager.fetchingPlayer) and (not self.manager.fetchingGames):
            self.movie.stop()
            self.hide()