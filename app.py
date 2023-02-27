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

# Scale app size on different screen resolutions.
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
    
    ## Update components on screen when information is edited by user.
    
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
        
    ##
        
    def delete_task(self):
        # Delete the task indicated by the user.
        
        # Check that the task number is a valid number.
        try:
            task_num = int(self.ui.task_num.text())
        except ValueError:
            return "INTEGER INPUT REQUIRED"
        
        # Update task lists and screen.
        user_profile.user.delete_task(task_num)
        self.tasks = user_profile.user.task_list
        self.show_tasks()
        
    def add_task(self):
        
        # Check if there are any tasks in the list.
        try:
            task_1 = self.tasks[0]
        except IndexError:
            task_1 = "pass"
            
        # Check that the task does have text.
        if self.ui.task_name.text() != "":
            user_profile.user.add_task(self.ui.task_name.text())
        else:
            user_profile.user.add_task("Empty task.")
        if task_1[0] == "":
            user_profile.user.delete_task(1)
            
        # Update task lists and screen.
        self.tasks = user_profile.user.task_list
        self.ui.task_name.setText("")
        self.show_tasks()
        
    def move_task_up(self):
        
        # Check that there are tasks in the list of tasks.
        try:
            task_1 = self.tasks[0]
        except IndexError:
            task_1 = "pass"
        
        # Check that the task number is a valid number.
        try:
            task_num = int(self.ui.task_num.text())
        except ValueError:
            return "INTEGER INPUT REQUIRED"
        
        # Update the user task list.
        user_profile.user.insert_task(task_num, task_num - 1)
        
        if task_1[0] == "":
            user_profile.user.delete_task(1)
        
        # Change the task number is the user box to match the new task number. Bound it to keep it reasonable.
        if task_num <= 1:
            self.ui.task_num.setText("1")
        else:
            self.ui.task_num.setText(f"{task_num - 1}")
            
        # Update the tasks list and the screen.
        self.tasks = user_profile.user.task_list
        self.show_tasks()
        
    def move_task_down(self):
        
        # Check that there are tasks in the list of tasks.
        try:
            task_1 = self.tasks[0]
        except IndexError:
            task_1 = "pass"
            
        # Check that the task number is a valid number.
        try:
            task_num = int(self.ui.task_num.text())
        except ValueError:
            return "INTEGER INPUT REQUIRED"
        
        # Update the user task list.
        user_profile.user.insert_task(task_num, task_num + 1)
        self.tasks = user_profile.user.task_list
        
        if task_1[0] == "":     
            user_profile.user.delete_task(1)
            
        # Change the task number is the user box to match the new task number. Bound it to keep it reasonable.
        if task_num >= len(self.tasks):
            self.ui.task_num.setText(f"{len(self.tasks)}")
        else:
            self.ui.task_num.setText(f"{task_num + 1}")
        
        # Update the screen with the new task list.
        self.show_tasks()
    
    def timer_input(self):
        
        # Validate user inputs for hours and minutes.
        try:
            
            # Automatically set empty text to zero.
            if self.ui.hour.text() == "":
                hours = 0
            else:
                hours = int(self.ui.hour.text())
                
            # Automatically set empty text to zero.
            if self.ui.min.text() == "":
                minutes = 0
            else:    
                minutes = int(self.ui.min.text())
            
            # If the time equals zero seconds, do not run the timer.
            if minutes == 0 and hours == 0:
                the_feared_error = int("e")
        
        # Reset the minute and hour inputs if invalid.
        except ValueError:
            self.ui.hour.setText("")
            self.ui.min.setText("")
            return "ERROR: INVALID INPUTS"
        
        # Else, set the values for hours and minutes.
        self.hour = hours
        self.minute = minutes
        
        # Run the timer widget window and hide the main window.
        self.timer_ui = tWindow()
        self.timer_ui.show()
        window.hide()
        
    def edit_task(self):
        
        # Check that the task number is a valid number.
        try:
            task_num = int(self.ui.task_num.text())
        except ValueError:
            return "INTEGER INPUT REQUIRED"
        
        
        # Check that there are tasks in the list.
        try:
            task_1 = self.tasks[0]
        except IndexError:
            task_1 = "pass"
            
        # Reset the first task if it is empty.
        if task_1[0] == "":
            user_profile.user.delete_task(1)
        
        # Search for the task.
        if task_num > 0 and task_num <= len(self.tasks):
            
            # Check that the new task name is valid.
            if "_" not in self.ui.task_name.text():
                
                # Make sure that the task name is not empty.
                if self.ui.task_name.text() != "":
        
                    user_profile.user.task_list[task_num - 1][0] = self.ui.task_name.text()
                    
                # Set the task name to "Empty Task" if the task name is empty.
                else:
                    user_profile.user.task_list[task_num - 1][0] = "Empty task."
                    
                # Update the user tasks list and screen.
                self.tasks = user_profile.user.task_list
                self.show_tasks()
    
    def update_time(self):
        
        # Run while the application is running.
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
                
# Create the timer widget window.
class tWindow(QWidget):

    # Create initial app conditions.
    def __init__(self):
        
        # Set up the application.
        QWidget.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.run = True
        
        # Set up the mica effect.
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
        
        # Show the current task at hand.
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
        
        # Retrieve all values in the user_data CSV file.
        name = csv_data.pull_csv_data("user_data.csv", 0, "name", 1)
        music = csv_data.pull_csv_data("user_data.csv", 0, "music", 1)
        time_complete = int(csv_data.pull_csv_data("user_data.csv", 0, "totalTime", 1))
        project_name = csv_data.pull_csv_data("user_data.csv", 0, "project", 1)
        
        # Update the user profile with the new number of seconds completed.
        user_profile.user.time_completed = int(time_complete) + time_elapsed
        
        # Update the user_data CSV file with the new number of seconds elapsed.
        csv_data.rewrite_csv_data("user_data.csv", [f"name,{name}", f"totalTime,{int(time_complete) + time_elapsed}", f"music,{music}", f"project,{project_name}"], '\n')
        
        # Display the floor of the number of hours the timer was used.
        window.ui.total_time.setText(str(math.floor((time_complete + time_elapsed) / 3600)))
        
        # Final Check: Update the user profile with the new number of seconds completed.
        user_profile.user.time_completed = time_complete + time_elapsed
        
        # Finish off all running threads.
        timer.kill_thread = True
        
        # Show the main window and hide this window.
        self.hide()
        self.run = False
        window.show()
        
    def update_project_name(self):
        # Update the project name when edited.
        user_profile.user.project_name = self.ui.project_name.text()
        
    def update_hour_min(self):
        
        # Run while the timer is running.
        while self.run:
            
            # Retrieve the number of seconds remaining in the timer.
            seconds = csv_data.pull_csv_data("vals.csv", 0, "time", 1)
            
            # Ensure that the retrieved value is not modified.
            if self.ui.seconds.text() != str(seconds) and str(seconds) != "PLACEHOLDER":
                self.ui.seconds.setText(str(seconds))
                
            # Ensure time is not set to a placeholder.
            elif self.ui.seconds.text() == "PLACEHOLDER":
                # Attempt to pull data again.
                seconds = csv_data.pull_csv_data("vals.csv", 0, "time", 1)
                
                # Update timer.
                self.ui.seconds.setText(str(seconds))
            
            # Update the time remaining.
            self.current_time_left = timer.time_left
            time.sleep(0.01)
            
            # Update the timer whenever there is a change.
            if self.ui.seconds.text() == "0" or self.ui.seconds.text() == "00":
                self.timer_stopped()
        
    def pause_timer(self):
        
        # Pause the timer if not already paused.
        if not self.paused:
            
            # Determine the number of seconds left.
            self.current_time_left = timer.time_left
            
            # Stop the threads and create a paused state.
            self.run = False
            timer.kill_thread = True
            self.paused = True
        
        # Unpause the timer when it is paused.
        else:
            
            # Restart the countdowns from where they left off.
            time_api.create_countdown(self.current_time_left)
            self.run = True
            update_time_thread = threading.Thread(target=self.update_hour_min)
            update_time_thread.start()
            
            # End the paused state.
            self.paused = False
        
    def update_titlebar(self):
        
        # Update changes to titlebar.
        self.setWindowTitle(f"Anti-Procrastinator: {self.ui.project_name.text()}")
        window.setWindowTitle(f"Anti-Procrastinator: {self.ui.project_name.text()}")
        window.ui.project_name.setText(f"{self.ui.project_name.text()}")
        self.update_project_name()
        
    def show_task(self):
        
        # Show the task at the top of the task list.
        task_text = ""
        if len(self.tasks) > 0:
            task_text = f"{self.tasks[0][0]}"
        self.ui.all_tasks.setPlainText(task_text)
        
    def finish_tasks(self):
        
        # Delete the task.
        window.ui.task_num.setText("1")
        window.delete_task()
        
        # Update the task screen in the main window (hidden).
        window.show_tasks()
        window.task_clear()
        
        # Show the new task the user is to complete.
        self.show_task()
        
    def skip_task(self):
        
        # Send the current (top) task to the end of the list.
        if len(user_profile.user.task_list) > 0:
            user_profile.user.insert_task(1, len(user_profile.user.task_list))
            
            # Update the main window screen and the timer widget screen.
            window.show_tasks()
            self.show_task()
            
# Create and run the application from windows class.
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    
    # Enable the mica effect, based on light vs dark theme of user system.
    hwnd = window.winId()
    win32mica.ApplyMica(hwnd, darkdetect.isDark())
    
    # Execute the app.
    app.exec_()
    
    # Store user information when application is exited.
    user_profile.store_data(user_profile.user)
