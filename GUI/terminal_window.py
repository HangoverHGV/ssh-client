from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPlainTextEdit, QLineEdit, QPushButton


class TerminalWindow(QMainWindow):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
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

        self.command_input = QLineEdit(self, placeholderText='Enter command')
        main_layout.addWidget(self.command_input)

        self.send_button = QPushButton('Send', self)
        self.send_button.clicked.connect(self.send_command)
        main_layout.addWidget(self.send_button)

        central_widget.setLayout(main_layout)

    def append_text(self, text):
        self.terminal_output.appendPlainText(text)

    def send_command(self):
        command = self.command_input.text()
        if command:
            stdin, stdout, stderr = self.connection.exec_command(command)
            output = stdout.read().decode()
            self.append_text(output)
            self.command_input.clear()
