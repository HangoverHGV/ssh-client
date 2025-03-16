from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QDesktopWidget)


class ConfigDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Settings')
        self.setGeometry(100, 100, 400, 300)
        self.center()
        self.parent = parent
        self.init_ui()
        self.load_settings()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)


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
        appearance = settings.get('appearance', {})
        theme = appearance.get('theme', 'Dark')
        font_size = appearance.get('font_size', '12')
        self.theme_dropdown.setCurrentText(theme)
        self.font_size_text.setText(str(font_size))

    def on_save(self):
        theme = self.theme_dropdown.currentText()
        font_size = self.font_size_text.text()
        self.parent.save_configs_json(self.parent.settings_file, {'theme': theme, 'font_size': font_size}, 'appearance')
        self.parent.apply_theme(theme)
        self.parent.apply_font_size(font_size)
        self.close()

