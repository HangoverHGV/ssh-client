from PySide6.QtWidgets import (QMainWindow, QLabel, QHBoxLayout, QWidget, QLineEdit, QVBoxLayout, QPushButton,
                                QApplication, QFileDialog)
from GUI.terminal_window import TerminalWindow
import multiprocessing as mp


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SSH-Client')
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 20)
        main_layout.setSpacing(1)

        # First row
        first_row_layout = QHBoxLayout()
        self.label = QLabel("Hostname:", self)
        first_row_layout.addWidget(self.label)

        main_layout.addLayout(first_row_layout)

        # Second row
        second_row_layout = QHBoxLayout()
        self.ip_input = QLineEdit(self, placeholderText='Enter hostname or IP')
        self.ip_input.setFixedWidth(200)
        second_row_layout.addWidget(self.ip_input)

        self.port_input = QLineEdit(self, placeholderText='Enter port')
        self.port_input.setFixedWidth(100)
        second_row_layout.addWidget(self.port_input)

        self.connect_button = QPushButton('Connect', self)
        self.connect_button.clicked.connect(self.ssh_connect)
        second_row_layout.addWidget(self.connect_button)

        main_layout.addLayout(second_row_layout)

        # Third row
        third_row_layout = QHBoxLayout()
        self.private_key_lbl = QLabel("Private Key:", self)
        third_row_layout.addWidget(self.private_key_lbl)

        self.private_key_path = QLineEdit(self, placeholderText='Select private key file')
        self.private_key_path.setFixedWidth(200)
        third_row_layout.addWidget(self.private_key_path)

        self.browse_button = QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse_file)
        third_row_layout.addWidget(self.browse_button)

        main_layout.addLayout(third_row_layout)

        central_widget.setLayout(main_layout)

    def browse_file(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Select Private Key File", "", "All Files (*)")
        if file_path:
            self.private_key_path.setText(file_path)

    def ssh_connect(self):
        host = self.ip_input.text()
        user = ''
        if '@' in host:
            user, host = host.split('@')
        port = self.port_input.text() or '22'
        private_key = self.private_key_path.text()

        self.start_terminal(host, user, port, private_key)

    def start_terminal(self, host, user, port, private_key):
        self.terminal_process = mp.Process(target=open_terminal, args=(host, user, port, private_key))
        self.terminal_process.start()
        self.terminal_process.join()

def open_terminal(host, user, port, private_key):
    app = QApplication([])
    terminal_window = TerminalWindow(host, user, port, private_key)
    terminal_window.show()
    app.exec()

