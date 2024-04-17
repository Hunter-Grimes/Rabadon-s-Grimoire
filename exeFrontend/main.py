from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PySide6.QtCore import QThreadPool
from PySide6.QtGui import QScreen

from profilePage import ProfilePageManager
from patchNotesPage import PatchNotesPage
from lobbyPage import LobbyPage

from callLocalRiotAPI import waitForLogin, lobbyListener

import requests

class MainWindow(QMainWindow):
    BASE_URL = "http://127.0.0.1:8080"
    def __init__(self, summoner):
        super().__init__()
        self.summoner = summoner
        self.threadPool = QThreadPool()
        
        self.resize(1280, 720)
        
        self.tabs = QTabWidget()
        
        myPUUID = requests.get(self.BASE_URL + "/user/by-riotID/" + summoner['tagLine'] + "/" + summoner['gameName']).json()['PUUID']
        
        self.tabs.addTab(ProfilePageManager(myPUUID, self.BASE_URL, self.threadPool), "Profile")
        self.tabs.addTab(PatchNotesPage(), "Patch Notes")
        
        # info = requests.get(self.BASE_URL + "/champ-select/generic/" + "895").json()
        # info['role'] = 'BOTTOM'
        # self.tabs.addTab(LobbyPage(self.threadPool, self.summoner, self.BASE_URL), "Test")
        
        with open("exeFrontend/tabStyle.qss", "r") as f:
            _style = f.read()
            self.tabs.setStyleSheet(_style)

        self.setCentralWidget(self.tabs)
        
        self.lobby = lobbyListener()
        self.lobby.signals.result.connect(self.lobbyCreated)
        self.threadPool.start(self.lobby)
        
        self.center()

    def lobbyCreated(self):
        self.tabs.addTab(LobbyPage(self.threadPool, self.summoner, self.BASE_URL), "Lobby")
        self.tabs.setCurrentIndex(2)
        
    def center(self):
        qr = self.frameGeometry()
        cp = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QApplication([])
    loader = QUiLoader()  # noqa: F841 
    
    summoner = waitForLogin()
    # summoner = {'tagLine': 'NA1', 'gameName': 'Potilwalda', 'puuid': 'b0ef40cf-ec56-5fbf-b74c-b838f180464f'}
    
    window = MainWindow(summoner)
    app.aboutToQuit.connect(window.lobby.clientClosed)
    window.setWindowTitle("Rabadon's Grimoire")
    
    window.show()
    app.exec()


if __name__ == '__main__':
    main()