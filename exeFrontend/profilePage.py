from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea, QGroupBox, QSpacerItem


class ProfilePage(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        # layout.addWidget(QLabel("Profile Page"))
        # self.setLayout(layout)
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
        layout.addWidget(QLabel("Match"))
        self.setLayout(layout)
