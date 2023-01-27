# Imports - Libraries
import sys, os, math, time, threading, win32mica, cgitb, PyQt5
from win32mica import MICAMODE, ApplyMica
from datetime import datetime
import darkdetect
from PyQt5 import  QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow

# Imports - My Modules
from ui_app_ui_2 import Ui_MainWindow
from ui_time_ui import Ui_Form
import user_profile
import csv_data
import timer
import time_api
import math

# Enable better error logs and debugging.
cgitb.enable(format = 'text')
win32mica.debugging = True

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
        #self.setWindowOpacity(0.99)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.timer_ui = None
        
        # Set up profile and user.        
        user_profile.initiate_user()
        self.ui.name.setText(user_profile.user.name)
        self.ui.total_time.setText(str(math.floor(user_profile.user.time_completed / 3600)))
        self.ui.project_name.setText(user_profile.user.project_name)
        self.tasks = user_profile.user.task_list
        
        # Add all previous tasks to screen.
        self.show_tasks()
        self.hour = 0
        self.minute = 0
            
        
        # Modifications to Window
        self.setWindowTitle(f"Anti-Procrastination: {self.ui.project_name.text()}")
        #self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setFixedSize(630, 390)
        
        # Create keybindings.
        self.ui.clear.clicked.connect(self.task_clear)
        self.ui.project_name.textChanged.connect(self.update_titlebar)
        self.ui.name.textChanged.connect(self.update_name)
        self.ui.enter.clicked.connect(self.add_task)
        self.ui.delete_bt.clicked.connect(self.delete_task)
        self.ui.up_bt.clicked.connect(self.move_task_up)
        self.ui.down_bt.clicked.connect(self.move_task_down)
        self.ui.start_bt.clicked.connect(self.timer_input)
        self.ui.editTask.clicked.connect(self.edit_task)
        
        # Run application threads.
        current_time_thread = threading.Thread(target=self.update_time)
        current_time_thread.start()

        # Show the application on the screen.
        self.show()
        # self.ui.error_console.hide()
    
    ## INIT FUNCTION ENDS ##

    def update_name(self):
        user_profile.user.name = self.ui.name.text()
        
    def update_project_name(self):
        user_profile.user.project_name = self.ui.project_name.text()

    def update_titlebar(self):
        self.setWindowTitle(f"Anti-Procrastinator: {self.ui.project_name.text()}")
        self.update_project_name()

    def task_clear(self):
        self.ui.task_name.setText("")
        self.ui.task_num.setText("")
        
    def show_tasks(self):
        task_text = ""
        task_num = 0
        for task in self.tasks:
            squiggles = ""
            for squiggle in range(0, len(f"Task {task_num + 1}:")):
                squiggles = f"{squiggles}~"
            task_text = f"{task_text}Task {task_num+1}: {task[0]}\n{squiggles}\n"
            task_num += 1
        self.ui.all_tasks.setPlainText(task_text)
        
    def delete_task(self):
        try:
            task_num = int(self.ui.task_num.text())
        except ValueError:
            return "INTEGER INPUT REQUIRED"
        
        user_profile.user.delete_task(task_num)
        self.tasks = user_profile.user.task_list
        self.show_tasks()
        
    def add_task(self):
        try:
            task_1 = self.tasks[0]
        except IndexError:
            task_1 = "pass"
        if self.ui.task_name.text() != "":
            user_profile.user.add_task(self.ui.task_name.text())
        else:
            user_profile.user.add_task("Empty task.")
        if task_1[0] == "":
            user_profile.user.delete_task(1)
        self.tasks = user_profile.user.task_list
        self.ui.task_name.setText("")
        self.show_tasks()
        
    def move_task_up(self):
        try:
            task_1 = self.tasks[0]
        except IndexError:
            task_1 = "pass"
            
        try:
            task_num = int(self.ui.task_num.text())
        except ValueError:
            return "INTEGER INPUT REQUIRED"
        
        user_profile.user.insert_task(task_num, task_num - 1)
        
        if task_1[0] == "":
            user_profile.user.delete_task(1)
            
        if task_num <= 1:
            self.ui.task_num.setText("1")
        else:
            self.ui.task_num.setText(f"{task_num - 1}")
            
        self.tasks = user_profile.user.task_list
        self.show_tasks()
        
    def move_task_down(self):
        try:
            task_1 = self.tasks[0]
        except IndexError:
            task_1 = "pass"
            
        try:
            task_num = int(self.ui.task_num.text())
        except ValueError:
            return "INTEGER INPUT REQUIRED"
        
        user_profile.user.insert_task(task_num, task_num + 1)
        
        self.tasks = user_profile.user.task_list
        
        if task_1[0] == "":     
            user_profile.user.delete_task(1)
            
        if task_num >= len(self.tasks):
            self.ui.task_num.setText(f"{len(self.tasks)}")
        else:
            self.ui.task_num.setText(f"{task_num + 1}")
        
        self.show_tasks()
    
    # Check timer input.
    def timer_input(self):
        try:
            if self.ui.hour.text() == "":
                hours = 0
            else:
                hours = int(self.ui.hour.text())
            if self.ui.min.text() == "":
                minutes = 0
            else:    
                minutes = int(self.ui.min.text())
            
            if minutes == 0 and hours == 0:
                the_feared_error = int("ᕦ(ò_óˇ)ᕤ")
            
        except ValueError:
            self.ui.hour.setText("")
            self.ui.min.setText("")
            return "ERROR: INVALID INPUTS"
        
        self.hour = hours
        self.minute = minutes
        
        self.timer_ui = tWindow()
        self.timer_ui.show()
        window.hide()
        
    def edit_task(self):
        try:
            task_num = int(self.ui.task_num.text())
        except ValueError:
            return "INTEGER INPUT REQUIRED"
        
        try:
            task_1 = self.tasks[0]
        except IndexError:
            task_1 = "pass"
            
        if task_1[0] == "":
            user_profile.user.delete_task(1)
        
        if task_num > 0 and task_num <= len(self.tasks):
            
            if "_" not in self.ui.task_name.text():
                
                if self.ui.task_name.text() != "":
        
                    user_profile.user.task_list[task_num - 1][0] = self.ui.task_name.text()
                    
                else:
                    user_profile.user.task_list[task_num - 1][0] = "Empty task."
                    
                self.tasks = user_profile.user.task_list
                self.show_tasks()
    
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
                
class tWindow(QWidget):

    # Create initial app conditions.
    def __init__(self):
        
        # Set up the application.
        QWidget.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.run = True
        
        # Mica Effect
        thwnd = self.winId().__int__()
        win32mica.ApplyMica(thwnd, darkdetect.isDark())
        
        # Set up profile and user.        
        self.ui.project_name.setText(user_profile.user.project_name)
        self.tasks = user_profile.user.task_list
        self.paused = False
        self.current_time_left = timer.time_left
        
        # Modifications to Window
        self.setWindowTitle(f"Anti-Procrastination: {self.ui.project_name.text()}")
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setFixedSize(453, 99)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        
        # Show the task.
        self.show_task()
        
        # Create keybindings.
        self.ui.project_name.textChanged.connect(self.update_titlebar)
        self.ui.stop_bt.clicked.connect(self.timer_stopped)
        self.ui.pause_bt.clicked.connect(self.pause_timer)
        self.ui.finishTask.clicked.connect(self.finish_tasks)
        self.ui.skipTask.clicked.connect(self.skip_task)
        
        # Run the countdown timer.
        seconds = 3600 * window.hour + 60 * window.minute
        self.total_time = seconds
        self.ui.seconds.setText(str(seconds))
        time_api.create_countdown(seconds)
        
        # Run countdown threads.
        update_time_thread = threading.Thread(target=self.update_hour_min)
        update_time_thread.start()

    def timer_stopped(self):
        
        # Calculate and update the total time.
        time_elapsed = self.total_time - self.current_time_left
        
        name = csv_data.pull_csv_data("user_data.csv", 0, "name", 1)
        music = csv_data.pull_csv_data("user_data.csv", 0, "music", 1)
        time_complete = int(csv_data.pull_csv_data("user_data.csv", 0, "totalTime", 1))
        project_name = csv_data.pull_csv_data("user_data.csv", 0, "project", 1)
        
        user_profile.user.time_completed = int(time_complete) + time_elapsed
        
        csv_data.rewrite_csv_data("user_data.csv", [f"name,{name}", f"totalTime,{int(time_complete) + time_elapsed}", f"music,{music}", f"project,{project_name}"], '\n')
        
        window.ui.total_time.setText(str(math.floor((time_complete + time_elapsed) / 3600)))
        
        user_profile.user.time_completed = time_complete + time_elapsed
        
        # Manage the windows and deal with threads.
        self.hide()
        timer.kill_thread = True
        self.run = False
        window.show()
        print("Stopped!")
        
    def update_project_name(self):
        user_profile.user.project_name = self.ui.project_name.text()
        
    def update_hour_min(self):
        while self.run:

            seconds = csv_data.pull_csv_data("vals.csv", 0, "time", 1)
            if self.ui.seconds.text() != str(seconds) and str(seconds) != "ヾ(⌐■_■)ノ♪":
                self.ui.seconds.setText(str(seconds))
            
            # Update the time remaining.
            self.current_time_left = timer.time_left
            
            time.sleep(0.01)
            
            if self.ui.seconds.text() == "0" or self.ui.seconds.text() == "00":
                self.timer_stopped()
        
        print("thread killed")
        
    def pause_timer(self):
        
        if not self.paused:
            self.current_time_left = timer.time_left
            self.run = False
            timer.kill_thread = True
            self.paused = True
        
        else:
            time_api.create_countdown(self.current_time_left)
            self.run = True
            update_time_thread = threading.Thread(target=self.update_hour_min)
            update_time_thread.start()
            self.paused = False
        
    def update_titlebar(self):
        self.setWindowTitle(f"Anti-Procrastinator: {self.ui.project_name.text()}")
        window.setWindowTitle(f"Anti-Procrastinator: {self.ui.project_name.text()}")
        window.ui.project_name.setText(f"{self.ui.project_name.text()}")
        self.update_project_name()
        
    def show_task(self):
        task_text = ""
        if len(self.tasks) > 0:
            task_text = f"{self.tasks[0][0]}"
        self.ui.all_tasks.setPlainText(task_text)
        
    def finish_tasks(self):
        window.ui.task_num.setText("1")
        window.delete_task()
        window.show_tasks()
        window.task_clear()
        self.show_task()
        
    def skip_task(self):
        
        if len(user_profile.user.task_list) > 0:
            user_profile.user.insert_task(1, len(user_profile.user.task_list))
            
            window.show_tasks()
            self.show_task()
            
# Create and run the application from windows class.
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    hwnd = window.winId()
    win32mica.ApplyMica(hwnd, darkdetect.isDark())
    app.exec_()
    user_profile.store_data(user_profile.user)
