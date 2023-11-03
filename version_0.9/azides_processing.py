import alkynes_uploading
from clear import delete_extra_files
from my_logging import merge_logs
from styles import *
from time_functions import time_format

import time
from PyQt5 import QtWidgets, QtGui
from PyQt5.Qt import *
from rdkit import Chem


class ProcessWindow(QWidget):
    def __init__(self, azides_window, azides, alkynes_window=None):
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
        self.process_button.setText('Start azides processing')
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

        self.azides_window = azides_window
        self.alkynes_window = alkynes_window
        self.azides = azides

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.clicked.connect(self.back_step)
        self.back_button.setText('Back')
        self.back_button.setGeometry(30, 650, 95, 40)
        self.back_button.setStyleSheet(back_next_button_stylesheet)

        self.clear_log()
        self.clear_azides()
        self.log.setText('Azides molecules were successfully uploaded')

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
        self.show_log('Checking azide molecules...\n\n')
        total_azides = len(self.azides)
        self.show_log(f'Found {total_azides} records\n')

        damaged_smiles = 0
        good_azides = 0
        bad_azides = 0
        non_azides = 0

        for i, azide in enumerate(self.azides):
            self.progress_bar.setValue(round((i + 1) / total_azides * 100))
            if Chem.MolFromSmiles(azide) is None:
                self.show_log(f'Warning: could not parse molecule {azide}\n')
                damaged_smiles += 1
                continue
            group_count = azide.count('N=[N+]=[N-]')
            if group_count == 0:
                self.show_log(f'Warning: molecule {azide} contains no azide moiety\n')
                non_azides += 1
                continue
            if group_count > 1:
                self.show_log(f'Warning: molecule {azide} contains more than one azide moiety\n')
                bad_azides += 1
                continue
            good_azides += 1
            with open('good_azides.txt', 'a') as f:
                f.write(f'{azide}\n')
                f.close()
            self.log.moveCursor(QtGui.QTextCursor.End)

        end_time = time.time()
        hours, minutes, seconds = time_format(start_time, end_time)

        self.show_log('\n\n')
        self.show_log('====\n')
        self.show_log('Finished loading!\n')
        self.show_log(f'Time: {hours:02}:{minutes:02}:{seconds:02}\n')
        self.show_log(f'Successfully loaded {good_azides} azides ({round(good_azides / total_azides * 100, 2)}%)\n')
        self.show_log('Following molecules were dropped out:\n')
        self.show_log(
            f'{damaged_smiles} records contained damaged smiles ({round(damaged_smiles / total_azides * 100, 2)}%)\n')
        self.show_log(
            f'{non_azides} molecules contained no azide moiety ({round(non_azides / total_azides * 100, 2)}%)\n')
        self.show_log(
            f'{bad_azides} molecules contained more than one azide moiety({round(bad_azides / total_azides * 100, 2)}%)\n')

        self.activate_next()

    def clear_log(self):
        with open('azides_log.txt', 'w') as f:
            f.write('')
            f.close()

    def clear_azides(self):
        with open('good_azides.txt', 'w') as f:
            f.write('')
            f.close()

    def show_log(self, msg):
        with open('azides_log.txt', 'a') as f:
            f.write(msg)
            f.close()
        with open('azides_log.txt', 'r') as f:
            data = f.read()
            self.log.setText(data)
            f.close()

    def activate_next(self):
        self.next_button.setEnabled(True)
        self.next_button.setStyleSheet(back_next_button_stylesheet)

    def back_step(self):
        self.back_clicked = True
        self.close()
        self.azides_window.show()

    def next_step(self):
        self.next_clicked = True
        self.close()
        if self.alkynes_window is None:
            self.alkynes_window = alkynes_uploading.AlkynesWindow(self.azides_window, self)
        self.alkynes_window.show()
