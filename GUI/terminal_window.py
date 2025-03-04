from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPlainTextEdit


class TerminalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Terminal')
        self.setGeometry(150, 150, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        self.terminal_output = QPlainTextEdit(self)
        self.terminal_output.setReadOnly(True)
        main_layout.addWidget(self.terminal_output)

        central_widget.setLayout(main_layout)

    def append_text(self, text):
        self.terminal_output.appendPlainText(text)