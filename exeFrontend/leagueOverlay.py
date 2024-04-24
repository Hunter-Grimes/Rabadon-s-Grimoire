from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QPoint


class summonerTracker(QMainWindow):
    BASE_URL = "http://127.0.0.1:8080"
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        self.oldPos = self.pos()
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.3);")
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.oldPos = event.globalPosition().toTuple()
    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        delta = QPoint(event.globalPosition().toTuple()[0] - self.oldPos[0], event.globalPosition().toTuple()[1] - self.oldPos[1])
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toTuple()
        

if __name__ == "__main__":
    app = QApplication([])
    loader = QUiLoader()  # noqa: F841 
    window = summonerTracker()
    window.show()
    app.exec()
    
    # print(pwc.get())