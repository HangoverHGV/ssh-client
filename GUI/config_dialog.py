from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton)


class ConfigDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Settings')
        self.setGeometry(100, 100, 400, 300)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()

        hbox1 = QHBoxLayout()
        self.label = QLabel('Theme')
        hbox1.addWidget(self.label)
        self.theme_dropdown = QComboBox()
        self.theme_dropdown.addItems(['Dark', 'Light'])
        hbox1.addWidget(self.theme_dropdown)
        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        self.label = QLabel('Font Size')
        hbox2.addWidget(self.label)
        self.font_size_text = QLineEdit()
        hbox2.addWidget(self.font_size_text)
        vbox.addLayout(hbox2)

        hbox3 = QHBoxLayout()
        self.save_btn = QPushButton('Save')
        self.save_btn.clicked.connect(self.on_save)
        hbox3.addWidget(self.save_btn)
        vbox.addLayout(hbox3)

        self.setLayout(vbox)

    def load_settings(self):
        settings = self.parent.load_configs(self.parent.settings_file)
        connection = settings.get('appearance', {})
        self.theme_dropdown.setCurrentText(connection.get('theme', ''))
        self.font_size_text.setText(connection.get('font_size', ''))

    def on_save(self):
        theme = self.theme_dropdown.currentText()
        font_size = self.font_size_text.text()
        self.parent.save_configs(self.parent.settings_file, 'appearance', {'theme': theme, 'font_size': font_size})
        self.close()

