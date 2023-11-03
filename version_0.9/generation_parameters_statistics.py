import calculations
from clear import delete_extra_files
from my_logging import merge_logs
from styles import *

from PyQt5 import QtWidgets
from PyQt5.Qt import *


class ParametersStatisticsWindow(QWidget):
    def __init__(self, start_window, saving_options_window, selected_isomers, inner_alkynes_specification,
                 Lipinsky_descriptors, logBB_model, threshold, saving_format):
        super().__init__()

        self.setWindowTitle('NeuroClick')
        self.setFixedSize(600, 700)
        self.setObjectName("MainWindow")

        self.log = QtWidgets.QTextEdit(self)
        self.log.setGeometry(170, 100, 280, 290)
        self.log.setReadOnly(True)

        self.next_button = QtWidgets.QPushButton(self)
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setText('Next')
        self.next_button.setGeometry(480, 650, 95, 40)
        self.next_button.setStyleSheet(default_stylesheet)
        self.next_button.setEnabled(False)

        self.next_clicked = False
        self.back_clicked = False

        self.start_window = start_window
        self.saving_options_window = saving_options_window
        self.selected_isomers = selected_isomers
        self.inner_alkynes_specification = inner_alkynes_specification
        self.Lipinsky_descriptors = Lipinsky_descriptors
        self.logBB_model = logBB_model
        self.threshold = threshold
        self.saving_format = saving_format

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.clicked.connect(self.back_step)
        self.back_button.setText('Back')
        self.back_button.setGeometry(30, 650, 95, 40)
        self.back_button.setStyleSheet(back_next_button_stylesheet)

        self.clear_log()
        self.show_log('Chosen generation parameters:\n\n')
        self.process()

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

    def process(self):
        if self.selected_isomers == '1_4':
            self.show_log('1,4-isomers are generated\n')
        elif self.selected_isomers == '1_5':
            self.show_log('1,5-isomers are generated\n')
        else:
            self.show_log('Both 1,5- and 1,4-isomers are generated\n')

        if self.inner_alkynes_specification == 'ignore':
            self.show_log('Products for internal alkynes are omitted\n')
        else:
            self.show_log('Products for internal alkynes are kept\n')

        descriptors = ''
        if self.Lipinsky_descriptors['donors']:
            descriptors += '\n-HDonors'
        if self.Lipinsky_descriptors['acceptors']:
            descriptors += '\n-HAcceptors'
        if self.Lipinsky_descriptors['weight']:
            descriptors += '\n-Molecular weight'
        if self.Lipinsky_descriptors['logP']:
            descriptors += '\n-logP'
        if not self.Lipinsky_descriptors['donors'] and not self.Lipinsky_descriptors['acceptors'] \
                and not self.Lipinsky_descriptors['weight'] and not self.Lipinsky_descriptors['logP']:
            descriptors += '\n-None'

        self.show_log(f'Molecules are filtered according to Lipinsky rules: {descriptors}\n')

        if self.logBB_model == 'Clark':
            self.show_log('LogBB Clark will be calculated\n')
        else:
            self.show_log('LogBB Rishton will be calculated\n')

        try:
            self.threshold = float(self.threshold)
            self.show_log(f'Molecules with logBB  less than {self.threshold} will be dropped\n')
        except ValueError:
            self.show_log(f'Molecules with logBB  less than 0.3 will be dropped\n\n')
            self.show_log(f'Warning: chosen threshold value {self.threshold} is invalid, so threshold is set to 0.3\n')
            self.threshold = 0.3

        if self.saving_format == 'txt':
            self.show_log('An output file will be saved in .txt format\n')
        else:
            self.show_log('An output file will be saved in .csv format\n')

        self.activate_next()

    def clear_log(self):
        with open('parameters_log.txt', 'w') as f:
            f.write('')
            f.close()

    def show_log(self, msg):
        with open('parameters_log.txt', 'a') as f:
            f.write(msg)
            f.close()
        with open('parameters_log.txt', 'r') as f:
            data = f.read()
            self.log.setText(data)
            f.close()

    def activate_next(self):
        self.next_button.setEnabled(True)
        self.next_button.setStyleSheet(back_next_button_stylesheet)

    def back_step(self):
        self.back_clicked = True
        self.close()
        self.saving_options_window.show()

    def next_step(self):
        self.next_clicked = True
        self.close()
        self.calculations_window = calculations.CalculationsWindow(self.start_window, self, self.selected_isomers,
                                                                   self.inner_alkynes_specification,
                                                                   self.Lipinsky_descriptors, self.logBB_model,
                                                                   self.threshold, self.saving_format)
        self.calculations_window.show()
