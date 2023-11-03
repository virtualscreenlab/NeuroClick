import generation_parameters_statistics
from clear import delete_extra_files
from my_logging import merge_logs
from styles import *

from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import QRadioButton, QLabel


class SavingOptionsWindow(QWidget):
    def __init__(self, start_window, Clark_Rishton_selection_window, selected_isomers, inner_alkynes_specification,
                 Lipinsky_descriptors, logBB_model, threshold):
        super().__init__()

        self.setWindowTitle('NeuroClick')
        self.setFixedSize(600, 700)
        self.setObjectName("MainWindow")

        self.info_label = QLabel(self)
        self.info_label.setGeometry(170, 220, 253, 40)
        self.info_label.setText('How to save an output file?')

        self.txt_check = QRadioButton('.txt format (molecules only)', self)
        self.txt_check.setGeometry(170, 250, 253, 40)
        self.txt_check.setChecked(True)
        self.txt_check.toggled.connect(self.checked_txt)

        self.csv_check = QRadioButton('.csv format (molecules and descriptors)', self)
        self.csv_check.setGeometry(170, 280, 290, 65)
        self.csv_check.toggled.connect(self.checked_csv)

        self.inner_alkyne_specification = None

        self.next_button = QtWidgets.QPushButton(self)
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setText('Next')
        self.next_button.setGeometry(480, 650, 95, 40)
        self.next_button.setStyleSheet(back_next_button_stylesheet)

        self.next_clicked = False
        self.back_clicked = False

        self.start_window = start_window
        self.Clark_Rishton_selection_window = Clark_Rishton_selection_window
        self.selected_isomers = selected_isomers
        self.inner_alkynes_specification = inner_alkynes_specification
        self.Lipinsky_descriptors = Lipinsky_descriptors
        self.logBB_model = logBB_model
        self.threshold = threshold
        self.saving_format = 'txt'

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

    def checked_txt(self):
        if self.txt_check.isChecked():
            self.saving_format = 'txt'
            self.csv_check.setChecked(False)

    def checked_csv(self):
        if self.csv_check.isChecked():
            self.saving_format = 'csv'
            self.txt_check.setChecked(False)

    def back_step(self):
        self.back_clicked = True
        self.close()
        self.Clark_Rishton_selection_window.show()

    def next_step(self):
        self.next_clicked = True
        self.close()

        self.parameters_statistics_window = generation_parameters_statistics.ParametersStatisticsWindow(
            self.start_window, self,
            self.selected_isomers, self.inner_alkynes_specification, self.Lipinsky_descriptors, self.logBB_model,
            self.threshold, self.saving_format
        )
        self.parameters_statistics_window.show()
