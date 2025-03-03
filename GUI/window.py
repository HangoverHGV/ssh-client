import sys
from PySide6.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QWidget, QLineEdit, QVBoxLayout, QApplication


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
        main_layout.setContentsMargins(10, 10, 10, 20)  # Add space at the bottom
        main_layout.setSpacing(5)  # Reduce spacing between rows

        # First row
        first_row_layout = QHBoxLayout()
        self.label = QLabel("Hostname:", self)
        first_row_layout.addWidget(self.label)

        main_layout.addLayout(first_row_layout)

        # Second row
        second_row_layout = QHBoxLayout()
        self.ip_input = QLineEdit(self, placeholderText='Enter hostname or IP')
        second_row_layout.addWidget(self.ip_input)

        self.port_input = QLineEdit(self, placeholderText='Enter port')
        second_row_layout.addWidget(self.port_input)

        main_layout.addLayout(second_row_layout)

        central_widget.setLayout(main_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())