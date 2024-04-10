from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PySide6.QtCore import QThreadPool

from profilePage import ProfilePageManager
from patchNotesPage import PatchNotesPage

import requests

class MainWindow(QMainWindow):
    BASE_URL = "http://127.0.0.1:8080"
    
    def __init__(self):
        super().__init__()
        self.threadPool = QThreadPool()
        
        tabs = QTabWidget()
        
        myName = 'LessJnglMoreBush'
        myTag = 'NA1'

        myPUUID = requests.get(self.BASE_URL + '/user/by-riotID/' + myTag + '/' + myName).json()['PUUID']
        
        tabs.addTab(ProfilePageManager(myPUUID, self.BASE_URL, self.threadPool), "Profile")
        tabs.addTab(PatchNotesPage(), "Patch Notes")
        with open("exeFrontend/tabStyle.qss", "r") as f:
            _style = f.read()
            tabs.setStyleSheet(_style)

        self.setCentralWidget(tabs)


def main():
    app = QApplication([])
    loader = QUiLoader()  # noqa: F841
    window = MainWindow()
    window.setWindowTitle("Rabadon's Grimoire")
    window.show()
    app.exec()

if __name__ == '__main__':
    main()