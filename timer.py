# File Code by Pranav Verma #

# Imports
import time
import threading
import csv_data

# Global Variables
seconds_list = []
kill_thread = False


# Define a countdown function.
def countdown(seconds):
    """Creates a countdown timer, based off the value in the CSV file.

    Args:
        seconds (int): Number of seconds to count down from.
    """

    # Global Variables
    global kill_thread

    # Assign seconds variable to time_left.
    time_left = seconds

    # Run the countdown timer (ends when time runs out).
    while time_left > 0:

        # TODO: Delete when testing is over.
        print(time_left)

        # Count down one second.
        time_left -= 1

        # Wait for one second before removing another second.
        time.sleep(1)

        # End the countdown when starting the next countdown.
        if kill_thread:
            break


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
