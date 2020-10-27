from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5 import uic
from updater import Ui_Form
from os import stat


class MyTimer(QThread):
    checkFile = pyqtSignal()

    def __init__(self):
        super(MyTimer, self).__init__()
        self.keep_running = False
        self.update_interval = 1

    def run(self):
        self.keep_running = True
        while self.keep_running:
            self.checkFile.emit()
            self.sleep(self.update_interval)

    def stop(self):
        self.keep_running = False


class Window(QWidget, Ui_Form):
    def __init__(self):
        super(Window, self).__init__()
        self.main_ui = Ui_Form()
        self.main_ui.setupUi(self)
        self.setFixedSize(605, 264)

        # Setup thread object
        self.myThread = MyTimer()

        # Events
        self.main_ui.select_file.clicked.connect(self.select_file)
        self.main_ui.interval.valueChanged.connect(self.interval_changed)
        self.main_ui.start_timer.clicked.connect(self.start_timer)
        self.main_ui.stop_timer.clicked.connect(self.stop_timer)
        self.myThread.checkFile.connect(self.check_file)
        self.main_ui.one_time.clicked.connect(self.conv_on_demand)

        # Instance variables
        self.selected_file = ""
        self.out_file = ""
        self.last_size = 0
        self.last_modified = 0
        self.first_check = False

        # Let's see the beautiful widget
        self.show()

    def select_file(self):
        file, mask = QFileDialog.getOpenFileName(None, "Select UI", ("*.ui"))
        if file != "":
            self.selected_file = file
            self.main_ui.filename.setText(file)
            self.out_file = self.selected_file.strip(".ui") + ".py"
            self.first_check = True
            self.check_file()

    def interval_changed(self):
        self.myThread.update_interval = self.main_ui.interval.value()

    def start_timer(self):
        if self.selected_file == "":
            return
        self.myThread.start()
        print("Thread started")
        ss = self.main_ui.status.styleSheet()
        ss = ss.replace("rgb(80, 80, 80)", "green")
        self.main_ui.status.setStyleSheet(ss)

    def stop_timer(self):
        self.myThread.stop()
        print("Thread stopped")
        ss = self.main_ui.status.styleSheet()
        ss = ss.replace("green", "rgb(80, 80, 80)")
        self.main_ui.status.setStyleSheet(ss)

    def conv_on_demand(self):
        if self.selected_file == "":
            print("No file selected")
            return
        self.__convert_selected()

    def __convert_selected(self):
        with open(self.out_file, "wt") as out:
            uic.compileUi(self.selected_file, out)

        info = stat(self.selected_file)
        # Get the last modified and current size
        self.last_modified = info.st_mtime
        self.last_size = info.st_size

    def check_file(self):
        # First check, convert to .py and set starting point for monitoring
        if self.first_check:
            # Convert it to a .py file
            self.__convert_selected()
            # No need to force a convert anymore; just monitor now
            self.first_check = False
        else:
            # Not the first check; let's see if we need any converting
            info = stat(self.selected_file)
            cur_last_mod = info.st_mtime
            cur_size = info.st_size
            if cur_last_mod != self.last_modified or cur_size != self.last_size:
                print("File changed, updating.")
                self.__convert_selected()

    def closeEvent(self, event):
        self.myThread.stop()
        self.myThread.quit()
        event.accept()


app = QApplication([])
window = Window()
app.exec_()
