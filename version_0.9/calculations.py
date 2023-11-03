import click_reaction
import results
from clear import delete_extra_files
from my_logging import merge_logs
from styles import *

from PyQt5 import QtWidgets
from PyQt5.Qt import *


class CalculationsWindow(QWidget):
    def __init__(self, start_window, parameters_statistics_window, selected_isomers, inner_alkynes_specification,
                 Lipinsky_descriptors, logBB_model, threshold, saving_format, results_window=None):
        super().__init__()

        self.setWindowTitle('NeuroClick')
        self.setFixedSize(1000, 700)
        self.setObjectName("MainWindow")

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(170, 100, 700, 35)

        self.log = QtWidgets.QTextEdit(self)
        self.log.setGeometry(170, 180, 700, 290)
        self.log.setReadOnly(True)
        self.cursor = QTextCursor(self.log.document())
        self.log.setTextCursor(self.cursor)

        self.calculate_button = QtWidgets.QPushButton(self)
        self.calculate_button.setText('Get reaction products')
        self.calculate_button.clicked.connect(self.get_products)
        self.calculate_button.setGeometry(190, 470, 660, 50)
        self.calculate_button.setStyleSheet(upload_button_stylesheet)

        self.get_products_clicked = False
        self.back_clicked = False
        self.next_clicked = False

        self.start_window = start_window
        self.parameters_statistics_window = parameters_statistics_window
        self.selected_isomers = selected_isomers
        self.inner_alkynes_specification = inner_alkynes_specification
        self.Lipinsky_descriptors = Lipinsky_descriptors
        self.logBB_model = logBB_model
        self.threshold = threshold
        self.saving_format = saving_format
        self.results_window = results_window

        self.next_button = QtWidgets.QPushButton(self)
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setText('Next')
        self.next_button.setGeometry(880, 650, 95, 40)
        self.next_button.setStyleSheet(default_stylesheet)
        self.next_button.setEnabled(False)

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.clicked.connect(self.back_step)
        self.back_button.setText('Back')
        self.back_button.setGeometry(30, 650, 95, 40)
        self.back_button.setStyleSheet(back_next_button_stylesheet)

        self.clear_log()
        self.log.setText('All azide and alkyne molecules were processed')

    def closeEvent(self, event):
        if not self.back_clicked and not self.next_clicked:
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
        self.get_products_clicked = False
        self.back_clicked = False

    def clear_log(self):
        with open('products_log.txt', 'w') as f:
            f.write('')
            f.close()

    def show_log(self, msg):
        with open('products_log.txt', 'a') as f:
            f.write(msg)
            f.close()
        with open('products_log.txt', 'r') as f:
            data = f.read()
            self.log.setText(data)
            f.close()

    def get_products(self):
        self.clear_log()
        self.get_products_clicked = True
        click_reaction.reaction(self.selected_isomers, self.inner_alkynes_specification, self.Lipinsky_descriptors,
                                self.logBB_model, self.threshold, self.saving_format, self)

    def activate_next(self):
        self.next_button.setEnabled(True)
        self.next_button.setStyleSheet(back_next_button_stylesheet)

    def back_step(self):
        self.back_clicked = True
        self.close()
        self.parameters_statistics_window.show()

    def next_step(self):
        self.next_clicked = True
        self.close()
        if self.results_window is None:
            self.results_window = results.ResultsWindow(self.start_window, self, self.saving_format)
        self.results_window.show()
