from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from GUI.window import App
import sys
import os


def main():
    app = QApplication(sys.argv)
    ex = App()
    app_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(app_dir, 'icon.png')
    ex.setWindowIcon(QIcon(icon_path))
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
