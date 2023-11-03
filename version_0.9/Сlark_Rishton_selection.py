import saving_options
from clear import delete_extra_files
from my_logging import merge_logs
from styles import *

from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import QLabel, QRadioButton, QTextEdit


class ClarkRishtonSelectionWindow(QWidget):
    def __init__(self, start_window, Lipinsky_selection_window, selected_isomers,
                 inner_alkynes_specification, Lipinsky_descriptors):
        super().__init__()

        self.setWindowTitle('NeuroClick')
        self.setFixedSize(600, 700)
        self.setObjectName("MainWindow")

        self.info_label = QLabel(self)
        self.info_label.setGeometry(220, 190, 253, 40)
        self.info_label.setText('Select logBB model:')

        self.Clark_check = QRadioButton(self)
        self.Clark_check.setGeometry(220, 220, 253, 40)
        self.Clark_check.setText('Clark model')
        self.Clark_check.setChecked(True)
        self.Clark_check.toggled.connect(self.check_Clark)

        self.Rishton_check = QRadioButton(self)
        self.Rishton_check.setGeometry(220, 250, 253, 40)
        self.Rishton_check.setText('Rishton model')
        self.Rishton_check.toggled.connect(self.check_Rishton)

        self.threshold_edit = QTextEdit(self)
        self.threshold_edit.setGeometry(220, 290, 37, 31)
        self.threshold_edit.setText('0.3')

        self.threshold_label = QLabel(self)
        self.threshold_label.setGeometry(260, 290, 70, 30)
        self.threshold_label.setText('Threshold')

        self.next_button = QtWidgets.QPushButton(self)
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setText('Next')
        self.next_button.setGeometry(480, 650, 95, 40)
        self.next_button.setStyleSheet(back_next_button_stylesheet)

        self.next_clicked = False
        self.back_clicked = False

        self.start_window = start_window
        self.Lipinsky_selection_window = Lipinsky_selection_window
        self.selected_isomers = selected_isomers
        self.inner_alkynes_specification = inner_alkynes_specification
        self.Lipinsky_descriptors = Lipinsky_descriptors
        self.logBB_model = 'Clark'

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

    def check_Clark(self):
        if self.Clark_check.isChecked():
            self.logBB_model = 'Clark'
            self.Rishton_check.setChecked(False)

    def check_Rishton(self):
        if self.Rishton_check.isChecked():
            self.logBB_model = 'Rishton'
            self.Clark_check.setChecked(False)

    def back_step(self):
        self.back_clicked = True
        self.close()
        self.Lipinsky_selection_window.show()

    def next_step(self):
        self.next_clicked = True
        self.threshold = self.threshold_edit.toPlainText()
        self.close()
        self.saving_options_window = saving_options.SavingOptionsWindow(self.start_window, self, self.selected_isomers,
                                                                        self.inner_alkynes_specification,
                                                                        self.Lipinsky_descriptors, self.logBB_model,
                                                                        self.threshold)
        self.saving_options_window.show()
