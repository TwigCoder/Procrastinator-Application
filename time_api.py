# File Code by Pranav Verma #

# Imports
import time
# import csv
import timer
import csv_data


# Define a function to create a countdown.
def create_countdown(do_work):
    
    # Decide on the number of seconds for the countdown.
    # TODO: Make the seconds based on the user input from the app's GUI.
    match do_work:
        
        # Work Timer
        case True:
            seconds = 10
            
        # Break Timer
        case False:
            seconds = 5
    
    # Get the previous values before editing the CSV file.
    music_bool = csv_data.pull_csv_data("vals.csv", 0, "music", 1)
    user_intro_bool = csv_data.pull_csv_data("vals.csv", 0, "user_intro_done", 1)
    
    # Write the countdown seconds to the CSV file.
    csv_data.rewrite_csv_data('vals.csv', [f"time,{seconds}", f"music,{music_bool}"], '\n')
    
    # Run the countdown function from `timer.py`.
    timer.run_countdown_thread()


# Test Runs.
# TODO: Delete when done.
create_countdown(True)
time.sleep(11)
create_countdown(False)
time.sleep(3)
create_countdown(True)
