from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

from profilePage import ProfilePage
from patchNotesPage import PatchNotesPage

import requests

class MainWindow(QMainWindow):
    BASE_URL = "http://127.0.0.1:5000"
    
    def __init__(self):
        super().__init__()
        
        tabs = QTabWidget()
        
        myName = 'LessJnglMoreBush'
        myPUUID = requests.get(self.BASE_URL + '/user/by-name/' + myName).json()['PUUID']
        
        tabs.addTab(ProfilePage(myPUUID), "Profile")
        tabs.addTab(PatchNotesPage(), "Patch Notes")
        with open("exeFrontend/tabStyle.qss", "r") as f:
            _style = f.read()
            tabs.setStyleSheet(_style)

        self.setCentralWidget(tabs)


if __name__ == '__main__':
    app = QApplication([])
    loader = QUiLoader()
    window = MainWindow()
    window.setWindowTitle("Rabadon's Grimoire")
    window.show()
    app.exec()
