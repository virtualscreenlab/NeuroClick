import inner_bond_problem
from clear import delete_extra_files
from my_logging import merge_logs
from styles import *

from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import QRadioButton


class IsomersSelectionWindow(QWidget):
    def __init__(self, start_window, alkynes_process_window):
        super().__init__()

        self.setWindowTitle('NeuroClick')
        self.setFixedSize(600, 700)
        self.setObjectName("MainWindow")

        self.isomer_1_4_check = QRadioButton('Generate only 1,4-isomer', self)
        self.isomer_1_4_check.setGeometry(200, 220, 253, 40)
        self.isomer_1_4_check.toggled.connect(self.checked_1_4)

        self.isomer_1_5_check = QRadioButton('Generate only 1,5-isomer', self)
        self.isomer_1_5_check.setGeometry(200, 250, 253, 40)
        self.isomer_1_5_check.toggled.connect(self.checked_1_5)

        self.both_isomers_check = QRadioButton('Generate both isomers', self)
        self.both_isomers_check.setGeometry(200, 280, 253, 40)
        self.both_isomers_check.toggled.connect(self.checked_both)

        self.selected_isomers = []

        self.next_button = QtWidgets.QPushButton(self)
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setText('Next')
        self.next_button.setGeometry(480, 650, 95, 40)
        self.next_button.setStyleSheet(default_stylesheet)
        self.next_button.setEnabled(False)

        self.next_clicked = False
        self.back_clicked = False

        self.start_window = start_window
        self.alkynes_process_window = alkynes_process_window

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

    def checked_1_4(self):
        self.selected_isomers.clear()
        if self.isomer_1_4_check.isChecked():
            self.selected_isomers.append('1_4')
            self.isomer_1_5_check.setChecked(False)
            self.both_isomers_check.setChecked(False)
            self.next_button.setEnabled(True)
            self.next_button.setStyleSheet(back_next_button_stylesheet)

    def checked_1_5(self):
        self.selected_isomers.clear()
        if self.isomer_1_5_check.isChecked():
            self.selected_isomers.append('1_5')
            self.isomer_1_4_check.setChecked(False)
            self.both_isomers_check.setChecked(False)
            self.next_button.setEnabled(True)
            self.next_button.setStyleSheet(back_next_button_stylesheet)

    def checked_both(self):
        self.selected_isomers.clear()
        if self.both_isomers_check.isChecked():
            self.selected_isomers.append('both')
            self.isomer_1_4_check.setChecked(False)
            self.isomer_1_5_check.setChecked(False)
            self.next_button.setEnabled(True)
            self.next_button.setStyleSheet(back_next_button_stylesheet)

    def back_step(self):
        self.back_clicked = True
        self.close()
        self.alkynes_process_window.show()

    def next_step(self):
        if len(self.selected_isomers) != 1:
            raise Exception('Please, select exactly one configuration of isomers')
        self.next_clicked = True
        self.close()

        self.inner_bond_problem_window = inner_bond_problem.InnerBondProblemWindow(self.start_window, self,
                                                                                   self.selected_isomers[0])
        self.inner_bond_problem_window.show()
