# Imports - Libraries
import sys, os, time, threading, win32mica, cgitb, PyQt5
from win32mica import MICAMODE, ApplyMica
from datetime import datetime
import darkdetect
from PyQt5 import  QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow

# Imports - My Modules
from app_ui_2 import Ui_MainWindow
import user_profile
import csv_data
import timer
import time_api

# Enable better error logs.
cgitb.enable(format = 'text')

# Fix app size on different screen resolutions.
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

# Compiling ui file command: python.exe -m PyQt5.uic.pyuic app_ui.ui -o app_ui.py

# Create the application window instance.
class Window(QMainWindow):

    # Create initial app conditions.
    def __init__(self):
        
        # Set up the application.
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowOpacity(0.99)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        
        # Modifications to Window
        self.setWindowTitle("Anti-Procrastination")
        self.setFixedSize(630, 390)
        
        # Set up profile and user.        
        user_profile.initiate_user()
        self.ui.name.setText(user_profile.user.name)
        self.ui.total_time.setText(str(user_profile.user.time_completed))
        
        
        # Create keybindings.
        self.ui.clear.clicked.connect(self.task_clear)
        self.ui.project_name.textChanged.connect(self.update_titlebar)
        self.ui.name.textChanged.connect(self.update_name)
        
        # Run application threads.
        current_time_thread = threading.Thread(target=self.update_time)
        current_time_thread.start()

        # Show the application on the screen.
        self.show()
        # self.ui.error_console.hide()

    def update_name(self):
        user_profile.user.name = self.ui.name.text()

    def update_titlebar(self):
        self.setWindowTitle(f"Anti-Procrastinator: {self.ui.project_name.text()}")

    def task_clear(self):
        self.ui.task_name.setText("")
        self.ui.task_num.setText("")
    
    # Update the time constantly.
    def update_time(self):
        
        # Run while application running.
        while True:
            
            # Get current time information.
            current_date = datetime.now()
            hour = current_date.hour
            minute = current_date.minute

            # Get current day information.
            day_name = datetime.today().strftime("%a")
            day = current_date.day
            year = datetime.today().strftime("%Y")
            am_pm = datetime.today().strftime("%p")
            
            # Create 12-hour clock.
            if hour > 12:
                hour -= 12
            
            # Formatting the hours and minutes for aesthetics.
            if hour < 10:
                hour = f"0{hour}"
            if minute < 10:
               minute = f"0{minute}"
            
            # Update screen elements IF NECESSARY.
            if self.ui.time_input.text() != f"{hour}:{minute} {am_pm}":
                self.ui.time_input.setText(f"{hour}:{minute} {am_pm}")
            if self.ui.date.text() != f"{day_name} {day}, {year}":
                self.ui.date.setText(f"{day_name} {day}, {year}")
            
            # Update AM-PM buttons.
            if am_pm == "AM" and (self.ui.am_bt.isEnabled() == True):
                self.ui.am_bt.setDisabled(False)
                self.ui.pm_bt.setDisabled(True)
                self.ui.am_bt.setText("☀️")
                self.ui.pm_bt.setText("")
            elif am_pm == "PM" and (self.ui.pm_bt.isEnabled() == True):
                self.ui.pm_bt.setDisabled(False)
                self.ui.am_bt.setDisabled(True)
                self.ui.am_bt.setText("")
                self.ui.pm_bt.setText("🌚")
            
            
# Create and run the application from windows class.
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    hwnd = window.winId()
    win32mica.ApplyMica(hwnd, darkdetect.isDark())
    app.exec_()
    user_profile.store_data(user_profile.user)
