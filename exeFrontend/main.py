from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

from profilePage import ProfilePage
from patchNotesPage import PatchNotesPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        tabs = QTabWidget()
        
        tabs.addTab(ProfilePage(), "Profile")
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