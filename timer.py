# Imports
import time
import threading
import csv_data

# Global Variables
seconds_list = []
time_left = 0
kill_thread = False


# Define a countdown function.
def countdown(seconds):
    """Creates a countdown timer, based off the value in the CSV file.

    Args:
        seconds (int): Number of seconds to count down from.
    """

    # Global Variables
    global kill_thread
    global time_left

    # Assign seconds variable to time_left.
    time_left = seconds

    # Run the countdown timer (ends when time runs out).
    while time_left > 0:

        # Wait for one second before removing another second.
        time.sleep(1)
        
        # Get the previous values before editing the CSV file.
        music_bool = csv_data.pull_csv_data("vals.csv", 0, "music", 1)
        
        # Write the countdown seconds to the CSV file.
        csv_data.rewrite_csv_data('vals.csv', [f"time,{time_left}", f"music,{music_bool}"], '\n')

        # End the countdown when starting the next countdown.
        if kill_thread:
            time_left = 0
            break
        
        # Else, continue running the timer.
        else:
            # Count down one second.
            time_left -= 1


# Run the countdown timer as a thread.
def run_countdown_thread():
    """Runs the countdown timer as a thread.
    """

    # Pull the seconds argument from the CSV file.
    seconds = csv_data.pull_csv_data("vals.csv", 0, "time", 1)
    seconds_list.append(int(seconds))

    # If a countdown exists, end it.
    global kill_thread
    kill_thread = True

    # Waiting for the countdown to end.
    time.sleep(1.01)

    # Create a new countdown thread.
    kill_thread = False
    countdown_thread = threading.Thread(target=countdown, args=(seconds_list[-1],))

    # Start the thread.
    countdown_thread.start()
