import azides_processing
from clear import delete_extra_files
from my_logging import merge_logs
from styles import *

from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import QFileDialog


class AzidesWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('NeuroClick')
        self.setFixedSize(600, 700)
        self.setObjectName("MainWindow")

        self.input_azides = QtWidgets.QTextEdit(self)
        self.input_azides.setGeometry(150, 80, 280, 250)
        self.input_azides.textChanged.connect(self.activate_next)

        self.load_azides_button = QtWidgets.QPushButton(self)
        self.load_azides_button.clicked.connect(self.read_input_from_file)
        self.load_azides_button.setText('Upload azides')
        self.load_azides_button.setGeometry(170, 330, 243, 40)
        self.load_azides_button.setStyleSheet(upload_button_stylesheet)

        self.next_button = QtWidgets.QPushButton(self)
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setText('Next')
        self.next_button.setGeometry(480, 650, 95, 40)
        self.next_button.setStyleSheet(default_stylesheet)
        self.next_button.setEnabled(False)

        self.next_clicked = False
        self.process_window = None

    def closeEvent(self, event):
        if not self.next_clicked:
            reply = QMessageBox.question \
                (self, 'Confirm exit',
                 "Quit NeuroClick?",
                 QMessageBox.Yes,
                 QMessageBox.No)
            if reply == QMessageBox.Yes:
                merge_logs()
                delete_extra_files()
                event.accept()
            else:
                event.ignore()
        self.next_clicked = False

    def activate_next(self):
        text = self.input_azides.toPlainText()
        if text != '':
            self.next_button.setEnabled(True)
            self.next_button.setStyleSheet(back_next_button_stylesheet)
        else:
            self.next_button.setEnabled(False)
            self.next_button.setStyleSheet(default_stylesheet)

    def read_input_from_file(self):
        fname = QFileDialog.getOpenFileName(caption='Open file', directory='.')[0]
        try:
            f = open(fname, 'r')
            with f:
                data = f.read()
                self.input_azides.setText(data)
        except Exception:
            pass

    def next_step(self):
        self.next_clicked = True
        azides = self.input_azides.toPlainText().split('\n')
        self.close()
        self.process_window = azides_processing.ProcessWindow(self, azides)
        self.process_window.show()
