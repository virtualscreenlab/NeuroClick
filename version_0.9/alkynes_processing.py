import isomers_selection
from my_logging import merge_logs
from clear import delete_extra_files
from click_reaction import INNER_BOND_PATTERN
from styles import *
from time_functions import time_format

import time
from PyQt5 import QtWidgets, QtGui
from PyQt5.Qt import *
from rdkit import Chem


class ProcessWindow(QWidget):
    def __init__(self, start_window, alkynes_window, alkynes):
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

        self.process_button = QtWidgets.QPushButton(self)
        self.process_button.setGeometry(190, 470, 660, 50)
        self.process_button.setText('Start alkynes processing')
        self.process_button.setStyleSheet(upload_button_stylesheet)
        self.process_button.clicked.connect(self.process)

        self.next_button = QtWidgets.QPushButton(self)
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setText('Next')
        self.next_button.setGeometry(880, 650, 95, 40)
        self.next_button.setStyleSheet(default_stylesheet)
        self.next_button.setEnabled(False)

        self.next_clicked = False
        self.back_clicked = False

        self.start_window = start_window
        self.alkynes_window = alkynes_window
        self.alkynes = alkynes

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.clicked.connect(self.back_step)
        self.back_button.setText('Back')
        self.back_button.setGeometry(30, 650, 95, 40)
        self.back_button.setStyleSheet(back_next_button_stylesheet)

        self.clear_log()
        self.clear_alkynes()
        self.log.setText('Alkynes molecules were successfully uploaded')

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
        self.clear_log()
        start_time = time.time()
        self.show_log('Checking alkyne molecules...\n\n')
        total_alkynes = len(self.alkynes)
        self.show_log(f'Found {total_alkynes} records\n')

        damaged_smiles = 0
        good_alkynes = 0
        inner_alkynes = 0
        bad_alkynes = 0
        non_alkynes = 0

        for i, alkyne in enumerate(self.alkynes):
            self.progress_bar.setValue(round((i + 1) / total_alkynes * 100))
            if Chem.MolFromSmiles(alkyne) is None:
                self.show_log(f'Warning: could not parse molecule {alkyne}\n')
                damaged_smiles += 1
                continue
            group_count = alkyne.count('#')
            if group_count == 0:
                self.show_log(f'Warning: molecule {alkyne} contains no alkyne moiety\n')
                non_alkynes += 1
                continue
            if group_count > 1:
                self.show_log(f'Warning: molecule {alkyne} contains more than one alkyne moiety\n')
                bad_alkynes += 1
                continue
            if Chem.MolFromSmiles(alkyne).HasSubstructMatch(INNER_BOND_PATTERN):
                self.show_log(f'Warning: molecule {alkyne} contains internal alkyne\n')
                inner_alkynes += 1

            good_alkynes += 1
            with open('good_alkynes.txt', 'a') as f:
                f.write(f'{alkyne}\n')
                f.close()
            self.log.moveCursor(QtGui.QTextCursor.End)

        end_time = time.time()
        hours, minutes, seconds = time_format(start_time, end_time)

        self.show_log('\n\n')
        self.show_log('====\n')
        self.show_log('Finished loading!\n')
        self.show_log(f'Time: {hours:02}:{minutes:02}:{seconds:02}\n')
        if inner_alkynes != 0:
            self.show_log(
                f'Warning: found {inner_alkynes} internal alkynes ({round(inner_alkynes / total_alkynes * 100, 2)}%).'
                f'Additional handling specification required\n')
        self.show_log(f'Successfully loaded {good_alkynes} alkynes ({round(good_alkynes / total_alkynes * 100, 2)}%)\n')
        self.show_log('Following molecules were dropped out:\n')
        self.show_log(
            f'{damaged_smiles} records contained damaged smiles ({round(damaged_smiles / total_alkynes * 100, 2)}%)\n')
        self.show_log(
            f'{non_alkynes} molecules contained no alkyne moiety ({round(non_alkynes / total_alkynes * 100, 2)}%)\n')
        self.show_log(
            f'{bad_alkynes} molecules contained more than one alkyne moiety({round(bad_alkynes / total_alkynes * 100, 2)}%)\n')

        self.activate_next()

    def clear_log(self):
        with open('alkynes_log.txt', 'w') as f:
            f.write('')
            f.close()

    def clear_alkynes(self):
        with open('good_alkynes.txt', 'w') as f:
            f.write('')
            f.close()

    def show_log(self, msg):
        with open('alkynes_log.txt', 'a') as f:
            f.write(msg)
            f.close()
        with open('alkynes_log.txt', 'r') as f:
            data = f.read()
            self.log.setText(data)
            f.close()

    def activate_next(self):
        self.next_button.setEnabled(True)
        self.next_button.setStyleSheet(back_next_button_stylesheet)

    def back_step(self):
        self.back_clicked = True
        self.close()
        self.alkynes_window.show()

    def next_step(self):
        self.next_clicked = True
        self.close()
        self.isomers_selection_window = isomers_selection.IsomersSelectionWindow(self.start_window, self)
        self.isomers_selection_window.show()
