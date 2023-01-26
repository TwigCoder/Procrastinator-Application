# Imports
import time
import timer
import csv_data


# Define a function to create a countdown.
def create_countdown(seconds):
    """The official timer countdown function. To  be used commercially.

    Args:
        seconds (int): Time to run the tasks.
    """

    # Get the previous values before editing the CSV file.
    music_bool = csv_data.pull_csv_data("vals.csv", 0, "music", 1)
    
    # Write the countdown seconds to the CSV file.
    csv_data.rewrite_csv_data('vals.csv', [f"time,{seconds}", f"music,{music_bool}"], '\n')
    
    # Run the countdown function from `timer.py`.
    timer.run_countdown_thread()


# Test Runs.
# TODO: Delete when done.
#create_countdown(True)
#time.sleep(11)
#create_countdown(False)
#time.sleep(3)
#create_countdown(True)
