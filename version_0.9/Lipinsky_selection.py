import Сlark_Rishton_selection
from clear import delete_extra_files
from my_logging import merge_logs
from styles import *

from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import QLabel, QCheckBox


class LipinskySelectionWindow(QWidget):
    def __init__(self, start_window, inner_bond_problem_window, selected_isomers, inner_alkynes_specification):
        super().__init__()

        self.setWindowTitle('NeuroClick')
        self.setFixedSize(600, 700)
        self.setObjectName("MainWindow")

        self.info_label = QLabel(self)
        self.info_label.setGeometry(200, 190, 253, 40)
        self.info_label.setText('Select Lipinsky descriptors:')

        self.donors_check = QCheckBox(self)
        self.donors_check.setGeometry(200, 220, 253, 40)
        self.donors_check.setText('Donor hydrogen bonds <= 5')
        self.donors_check.toggled.connect(self.checked_donors)

        self.acceptors_check = QCheckBox(self)
        self.acceptors_check.setGeometry(200, 250, 253, 40)
        self.acceptors_check.setText('Acceptor hydrogen bonds <= 10')
        self.acceptors_check.toggled.connect(self.checked_acceptors)

        self.weight_check = QCheckBox(self)
        self.weight_check.setGeometry(200, 280, 253, 40)
        self.weight_check.setText('Molecular weight < 500 Da')
        self.weight_check.toggled.connect(self.checked_weight)

        self.logP_check = QCheckBox(self)
        self.logP_check.setGeometry(200, 310, 253, 40)
        self.logP_check.setText('logP <= 5')
        self.logP_check.toggled.connect(self.checked_logP)

        self.Lipinsky_descriptors = {'donors': False, 'acceptors': False, 'weight': False, 'logP': False}

        self.next_button = QtWidgets.QPushButton(self)
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setText('Next')
        self.next_button.setGeometry(480, 650, 95, 40)
        self.next_button.setStyleSheet(back_next_button_stylesheet)

        self.next_clicked = False
        self.back_clicked = False

        self.start_window = start_window
        self.inner_bond_problem_window = inner_bond_problem_window
        self.selected_isomers = selected_isomers
        self.inner_alkynes_specification = inner_alkynes_specification

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

    def checked_donors(self):
        if self.donors_check.isChecked():
            self.Lipinsky_descriptors['donors'] = True
        else:
            self.Lipinsky_descriptors['donors'] = False

    def checked_acceptors(self):
        if self.acceptors_check.isChecked():
            self.Lipinsky_descriptors['acceptors'] = True
        else:
            self.Lipinsky_descriptors['acceptors'] = False

    def checked_weight(self):
        if self.weight_check.isChecked():
            self.Lipinsky_descriptors['weight'] = True
        else:
            self.Lipinsky_descriptors['weight'] = False

    def checked_logP(self):
        if self.logP_check.isChecked():
            self.Lipinsky_descriptors['logP'] = True
        else:
            self.Lipinsky_descriptors['logP'] = False

    def back_step(self):
        self.back_clicked = True
        self.close()
        self.inner_bond_problem_window.show()

    def next_step(self):
        self.next_clicked = True
        self.close()
        self.Clark_Rishton_selection_window = Сlark_Rishton_selection.ClarkRishtonSelectionWindow(
            self.start_window,
            self,
            self.selected_isomers,
            self.inner_alkynes_specification,
            self.Lipinsky_descriptors)
        self.Clark_Rishton_selection_window.show()
