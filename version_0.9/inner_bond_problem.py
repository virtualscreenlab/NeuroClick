import Lipinsky_selection
from clear import delete_extra_files
from my_logging import merge_logs
from styles import *

from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import QRadioButton, QLabel


class InnerBondProblemWindow(QWidget):
    def __init__(self, start_window, isomers_selection_window, selected_isomers):
        super().__init__()

        self.setWindowTitle('NeuroClick')
        self.setFixedSize(600, 700)
        self.setObjectName("MainWindow")

        self.info_label = QLabel(self)
        self.info_label.setGeometry(200, 220, 253, 40)
        self.info_label.setText('What to do with internal alkynes?')

        self.ignore_check = QRadioButton('Ignore', self)
        self.ignore_check.setGeometry(200, 250, 253, 40)
        self.ignore_check.toggled.connect(self.checked_ignore)

        self.both_isomers_check = QRadioButton('Generate both isomers', self)
        self.both_isomers_check.setGeometry(200, 280, 253, 40)
        self.both_isomers_check.toggled.connect(self.checked_both)

        self.inner_alkyne_specification = None

        self.next_button = QtWidgets.QPushButton(self)
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setText('Next')
        self.next_button.setGeometry(480, 650, 95, 40)
        self.next_button.setStyleSheet(default_stylesheet)
        self.next_button.setEnabled(False)

        self.next_clicked = False
        self.back_clicked = False

        self.start_window = start_window
        self.isomers_selection_window = isomers_selection_window
        self.selected_isomers = selected_isomers

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

    def checked_ignore(self):
        if self.ignore_check.isChecked():
            self.inner_alkyne_specification = 'ignore'
            self.both_isomers_check.setChecked(False)
            self.next_button.setEnabled(True)
            self.next_button.setStyleSheet(back_next_button_stylesheet)

    def checked_both(self):
        if self.both_isomers_check.isChecked():
            self.inner_alkyne_specification = 'both'
            self.ignore_check.setChecked(False)
            self.next_button.setEnabled(True)
            self.next_button.setStyleSheet(back_next_button_stylesheet)

    def back_step(self):
        self.back_clicked = True
        self.close()
        self.isomers_selection_window.show()

    def next_step(self):
        if self.inner_alkyne_specification is None:
            raise Exception('Please, select a specification for inner alkynes')
        self.next_clicked = True
        self.close()

        self.Lipinsky_selection_window = Lipinsky_selection.LipinskySelectionWindow(self.start_window, self,
                                                                                        self.selected_isomers,
                                                                                        self.inner_alkyne_specification)
        self.Lipinsky_selection_window.show()
