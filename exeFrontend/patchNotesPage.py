from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
        
class PatchNotesPage(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Patch Notes"))
        self.setLayout(layout)