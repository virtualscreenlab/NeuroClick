import alkynes_processing
from clear import delete_extra_files
from my_logging import merge_logs
from styles import *

from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import QFileDialog


class AlkynesWindow(QWidget):
    def __init__(self, start_window, azides_process_window):
        super().__init__()

        self.setWindowTitle('NeuroClick')
        self.setFixedSize(600, 700)
        self.setObjectName("MainWindow")

        self.input_alkynes = QtWidgets.QTextEdit(self)
        self.input_alkynes.setGeometry(150, 80, 280, 250)
        self.input_alkynes.textChanged.connect(self.activate_next)

        self.load_alkynes_button = QtWidgets.QPushButton(self)
        self.load_alkynes_button.clicked.connect(self.read_input_from_file)
        self.load_alkynes_button.setText('Upload alkynes')
        self.load_alkynes_button.setGeometry(170, 330, 243, 40)
        self.load_alkynes_button.setStyleSheet(upload_button_stylesheet)

        self.next_button = QtWidgets.QPushButton(self)
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setText('Next')
        self.next_button.setGeometry(480, 650, 95, 40)
        self.next_button.setStyleSheet(default_stylesheet)
        self.next_button.setEnabled(False)

        self.next_clicked = False
        self.back_clicked = False

        self.start_window = start_window
        self.azides_process_window = azides_process_window
        self.azides_process_window.alkynes_window = self

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.clicked.connect(self.back_step)
        self.back_button.setText('Back')
        self.back_button.setGeometry(30, 650, 95, 40)
        self.back_button.setStyleSheet(back_next_button_stylesheet)

    def closeEvent(self, event):
        if not self.next_clicked and not self.back_clicked:
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
        self.back_clicked = False

    def activate_next(self):
        text = self.input_alkynes.toPlainText()
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
                self.input_alkynes.setText(data)
        except Exception:
            pass


    def back_step(self):
        self.back_clicked = True
        self.close()
        self.azides_process_window.show()

    def next_step(self):
        self.next_clicked = True
        alkynes = self.input_alkynes.toPlainText().split('\n')
        self.close()
        self.process_window = alkynes_processing.ProcessWindow(self.start_window, self, alkynes)
        self.process_window.show()
