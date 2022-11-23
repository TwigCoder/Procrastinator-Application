# File Code by Pranav Verma #

# Imports
import csv_data

# Global Variables
user = None


# Class that holds all the attributes of the user.
class User:
    """Class that initializes all the User attributes.
    """

    # Initialize the User profile with basic attributes.
    def __init__(self, name, time, music="basic", task_list=None):
        """Initializes the user profile.

        Args:
            name (str): Name of the user.
            time (int): Number of seconds the user has been in work and break mode..
            music (str, optional): Type of music the user listens to. Defaults to "basic".
            task_list (list, optional): List of tasks the user has created. Defaults to [].
        """
        if task_list is None:
            task_list = []
        self.name = name
        self.time_completed = time
        self.music = music
        self.task_list = task_list

    # Define a function to add tasks to the list.
    def add_task(self, task):
        """Add a task to the list of tasks the user owns. Cannot have an underscore in its description.

        Args:
            task (str): Task the user has created.

        Returns:
            str: Error message stating that the task is invalid.
        """

        # Check that there are no invalid characters.
        if "_" in task:
            # TODO GUI: Add popup that tells user that the task is invalid because of `_`.
            print("TASK IS INVALID")
            return "ERROR 001: INVALID TASK"

        # If valid, create the task.
        else:
            # Format: "Number: Task Name, Completion Status, Tags"
            self.task_list.append([str(len(self.task_list) + 1), task, "incomplete", "none"])

    # Define a function to remove tasks.
    def delete_task(self, task_num):
        """Delete a task the user has created.

        Args:
            task_num (str, int): Number of the task the user wishes to delete.
            
        Returns:
            str: Message stating whether the task was found or not.
        """

        # Convert the task number to a string.
        task_num = str(task_num)

        # Check all the tasks in the list.
        for task in self.task_list:

            # Delete task if it is the correct task.
            if task_num == task[0]:
                self.task_list.remove(task)
                return "Task found."

        # Report an error if the task was not found.
        print('ERROR: Task could not be found')
        # TODO GUI: Add a popup when error is formed.
        return 'ERROR 002: TASK NOT FOUND'

    # Create a list of tasks based off the values in `task_list.csv`.
    def create_tasks_list(self):
        """Creates the list of tasks from the previous session.
        """

        # Define the new list from previously stored data.
        try:
            tasks_list = csv_data.pull_csv_data("task_list.csv", 0, "tasks", 1)

        # If the list is empty, create a blank list.
        except IndexError:
            tasks_list = []

        # Ensure that tasks_list is not empty.
        if tasks_list == ' ':
            tasks_list = []

        # FORMAT: [ ["task_number", "task_name", "task_status", "tags"], [repeat for new task] ]

        # Check if tasks_list is empty.
        if len(tasks_list) == 0:
            pass

        # Continue if tasks_list is not empty.
        else:
            # Split task_list into separate components.
            tasks_list = tasks_list.split("_")  # type: ignore

            # Delete empty tasks.
            for task in tasks_list:
                if task == '':
                    tasks_list.remove(task)

            # Divide the tasks into groups of four.
            grouped_tasks = [tasks_list[i:i + 4] for i in range(0, len(tasks_list), 4)]

            # Add the grouped tasks to the User's task list.
            self.task_list = grouped_tasks

    # Define a function to return the type of music the user enjoys.
    def music_type(self):
        """Return the type of music the user enjoys listening to.

        Returns:
            str: Type of music the user listens to.
        """
        return self.music


# Define a function to initiate a new user to the application.
def initiate_user(name, music):
    """Initiates the new user with their name, music preference, and base stats.

    Args:
        name (str): Name of the user.
        music (str): Genre of music that they wish to listen to.
    """

    # Use the attributes to create a global User class.
    global user

    # Create the user class with base stats.
    user = User(name, 0, music, [])

    # Write to the CSV file that the user introduction is complete.

    time_complete = int(csv_data.pull_csv_data('user_data.csv', 0, "totalTime", 1))
    music = csv_data.pull_csv_data('user_data.csv', 0, "music", 1)

    csv_data.rewrite_csv_data("user_data.csv", [f"name,{name}", f"totalTime,0", f"music,{music}",
                                                f"user_intro_done,t"], '\n')


# Define a function to pull all the user information from the CSV file.
def create_user_profile(name=None, music=None):
    # Check that the user has completed the introduction.
    intro_done = csv_data.pull_csv_data("user_data.csv", 0, "user_intro_done", 1)

    # Change the intro_done variable from a string to a boolean.
    match intro_done:

        # Case: t = True
        case 't':
            intro_done = True

        # Case: f = False
        case 'f':
            intro_done = False

    # If they are not a new user, check for attributes in the CSV file.
    if intro_done:

        # Download all the basic attributes of the user.
        name = csv_data.pull_csv_data('user_data.csv', 0, "name", 1)
        time_complete = int(csv_data.pull_csv_data('user_data.csv', 0, "totalTime", 1))
        music = csv_data.pull_csv_data('user_data.csv', 0, "music", 1)

        # Use the attributes to create a global User class.
        global user
        user = User(name, time_complete, music, [])

        # Add previous tasks to the user.
        user.create_tasks_list()
        print(user.task_list)

    # If they are a new user, call the initiation function.
    if not intro_done:
        initiate_user(name, music)


# Define a function to store the user data when closing the app.
def store_data(user_class):

    # Find the user values for `vals.csv`.
    name = user_class.name
    time_complete = user_class.time_completed
    music = user_class.music
    user_intro = csv_data.pull_csv_data("user_data.csv", 0, "user_intro_done", 1)

    # Write the user values to `vals.csv`.
    csv_data.rewrite_csv_data('user_data.csv', [f"name,{name}", f"totalTime,{time_complete}", f"music,{music}",
                                           f"user_intro_done,{user_intro}"], '\n')

    # Prepare the tasks to be added to `task_list.csv`.
    all_tasks = ['tasks,']
    for task in user_class.task_list:
        print(task)
        for section in task:
            print(section)
            all_tasks.append(f"{section}")

    # Write all tasks down in `task_list.csv`.
    csv_data.rewrite_csv_data("task_list.csv", all_tasks, "_")


# TODO: Move this code to the main python file (where the app runs). Remember: create_user_profile requires args when
# TODO: the user is new.
# Create the User.
create_user_profile(name=None, music=None)
# TODO: Only store data when the app is closed. (Requires app GUI).
store_data(user)
