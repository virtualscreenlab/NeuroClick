from clear import delete_extra_files
from my_logging import merge_logs
from styles import *

from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import QFileDialog


class ResultsWindow(QWidget):
    def __init__(self, start_window, calculations_window, saving_format):
        super().__init__()

        self.setWindowTitle('NeuroClick')
        self.setFixedSize(600, 700)
        self.setObjectName("MainWindow")

        self.download_button = QtWidgets.QPushButton(self)
        self.download_button.clicked.connect(self.download_results)
        self.download_button.setText('Download file')
        self.download_button.setGeometry(170, 330, 243, 40)
        self.download_button.setStyleSheet(upload_button_stylesheet)

        self.restart_button = QtWidgets.QPushButton(self)
        self.restart_button.clicked.connect(self.restart_step)
        self.restart_button.setText('Restart')
        self.restart_button.setGeometry(480, 650, 95, 40)
        self.restart_button.setStyleSheet(back_next_button_stylesheet)

        self.restart_clicked = False
        self.back_clicked = False

        self.start_window = start_window
        self.calculations_window = calculations_window
        self.calculations_window.results_window = self
        self.saving_format = saving_format

        self.output_data = QtWidgets.QTextEdit(self)
        self.output_data.setGeometry(150, 80, 280, 250)
        if self.saving_format == 'csv':
            f = open('output.csv', 'r')
        else:
            f = open('output.txt', 'r')
        self.output_data.setText(f.read())

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.clicked.connect(self.back_step)
        self.back_button.setText('Back')
        self.back_button.setGeometry(30, 650, 95, 40)
        self.back_button.setStyleSheet(back_next_button_stylesheet)

    def closeEvent(self, event):
        if not self.restart_clicked and not self.back_clicked:
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
        self.restart_clicked = False
        self.back_clicked = False

    def download_results(self):
        text = self.output_data.toPlainText()
        fname = QFileDialog.getSaveFileName(caption='Save file', directory='.')[0]
        try:
            f = open(fname, 'w')
            f.write(text)
        except Exception:
            pass

    def back_step(self):
        self.back_clicked = True
        self.close()
        self.calculations_window.show()

    def restart_step(self):
        self.restart_clicked = True
        self.close()
        merge_logs()
        delete_extra_files()
        self.start_window.show()
        self.start_window.input_azides.setText('')
