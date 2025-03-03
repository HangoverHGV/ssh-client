from multiprocessing import Process
from PySide6.QtWidgets import QApplication
import sys

from GUI.window import App


def main():
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    process = Process(target=main)
    process.start()
