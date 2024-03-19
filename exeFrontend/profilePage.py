from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QScrollArea, QGroupBox
from PySide6.QtGui import QPixmap


class ProfilePage(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        scroll = QScrollArea()
        group = QGroupBox()
        
        boxlayout = QVBoxLayout()
        for _ in range(20):
            boxlayout.addWidget(Match())
        
        group.setLayout(boxlayout)
        scroll.setWidget(group)
        layout.addWidget(scroll)
        self.setLayout(layout)
        
class Match(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout()
        box = QGroupBox()
        box.setFixedSize(500, 150)
        boxLayout = QGridLayout()
        
        label = QLabel()
        pixmap = QPixmap('dragontailData/14.5.1/img/item/1001.png')
        pixmap = pixmap.scaled(50,50)
        label.setPixmap(pixmap)
        boxLayout.addWidget(label, 0, 0, -1, 1)
        
        label = QLabel("Victory")
        boxLayout.addWidget(label, 0, 1, -1, 1)
        
        label = QLabel("0/15/0")
        boxLayout.addWidget(label, 0, 2)
        
        label = QLabel("100cs - 40%kp")
        boxLayout.addWidget(label, 1, 2)
        
        itemBox = QGroupBox()
        items = QGridLayout()
        
        label = QLabel()
        pixmap = QPixmap('dragontailData/14.5.1/img/item/1001.png')
        pixmap = pixmap.scaled(30,30)
        label.setPixmap(pixmap)
        items.addWidget(label, 0, 0)
        
        label = QLabel()
        pixmap = QPixmap('dragontailData/14.5.1/img/item/1001.png')
        pixmap = pixmap.scaled(30,30)
        label.setPixmap(pixmap)
        items.addWidget(label, 0, 1)
        
        label = QLabel()
        pixmap = QPixmap('dragontailData/14.5.1/img/item/1001.png')
        pixmap = pixmap.scaled(30,30)
        label.setPixmap(pixmap)
        items.addWidget(label, 0, 2)
        
        label = QLabel()
        pixmap = QPixmap('dragontailData/14.5.1/img/item/1001.png')
        pixmap = pixmap.scaled(30,30)
        label.setPixmap(pixmap)
        items.addWidget(label, 1, 0)
        
        label = QLabel()
        pixmap = QPixmap('dragontailData/14.5.1/img/item/1001.png')
        pixmap = pixmap.scaled(30,30)
        label.setPixmap(pixmap)
        items.addWidget(label, 1, 1)
        
        label = QLabel()
        pixmap = QPixmap('dragontailData/14.5.1/img/item/1001.png')
        pixmap = pixmap.scaled(30,30)
        label.setPixmap(pixmap)
        items.addWidget(label, 1, 2)
        
        itemBox.setLayout(items)
        boxLayout.addWidget(itemBox, 0, 3, -1, 1)
        
        
        box.setLayout(boxLayout)
        layout.addWidget(box)
        self.setLayout(layout)
