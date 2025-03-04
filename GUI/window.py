from PySide6.QtWidgets import (QMainWindow, QLabel, QHBoxLayout, QWidget, QLineEdit, QVBoxLayout, QPushButton,
                                QFileDialog, QApplication)
from connection.ssh import ssh_connection
from GUI.terminal_window import TerminalWindow
from multiprocessing import Process


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
        connection_dict = {}
        host = self.ip_input.text()
        if '@' in host:
            user, host = host.split('@')
            connection_dict['user'] = user
        connection_dict['host'] = host
        port = self.port_input.text()
        if not port:
            port = 22
        connection_dict['port'] = port
        private_key = self.private_key_path.text()
        if private_key:
            connection_dict['private_key'] = private_key

        connection = ssh_connection(**connection_dict)
        if connection:
            self.open_terminal(connection)

    def open_terminal(self, connection):
        process = Process(target=self.start_terminal, args=(connection,))
        process.start()

    def start_terminal(self, connection):
        app = QApplication([])
        terminal_window = TerminalWindow(connection)
        terminal_window.show()
        app.exec()
