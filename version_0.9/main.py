import sys

from PyQt5.QtWidgets import QApplication
from azides_uploading import AzidesWindow


def application():
    app = QApplication(sys.argv)
    azides_window = AzidesWindow()
    azides_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    application()
