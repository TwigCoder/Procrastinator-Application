
## Contributors: Krish ##

#### DO NOT DELETE ####

#### DUE ON WEDNESDAY 28 ####

## REQUIREMENTS ##
# Fix the current errors (rewrite all the code you pushed yesterday lol)
# Call the user profile music preference.
# For music choice:
    # I asked for match-switch. You used if-else statements. Hilariously, you FAILED at creating if-else statements. Stop fighting and use the match-switch statement.
    # Honestly, your comments suck and you have no docstrings. Multiple comments for imports? and yet none for each option in the if-else statement?
# Next Task:
    # Create function that will check the CSV document `vals.csv` every second or nanosecond for when music CHANGES to t (true) or f (false).
        # You have to be aware when it CHANGES!!!
    # It should stop / start playing music when there is a change.
    # Music should loop and not end automatically.
    # You need to find more music files and add them.
        # Divide the locals folder into more folders. One of teh folders must be Default.
    # Create a folder in Music called UserMusic (next to Local, NOT in local.)
        # If User wants to play their music, that option will be USERMUSIC in their profile prefernences.
#### DO NOT DELETE THIS ANYONE ####

            


# Define a function to play music
# File-types: MP3, WAV, AIFF

#NOTE: Create a function that takes in a file name (music) as an argument.

# Imports the "User" class from "profile.py"
import profile



# Imports the sound playback module
from playsound import playsound

# Creates a function by the name of "play_music"
def play_music(file_name):
    
    # Whenever called, will load the playsound command for any file we want
    playsound(file_name)


# Plays a file based on user's choosing.
def music_choice():

    # When called when the timer starts running, plays a specific type of music based on the user's choosing.
        
    # Play the default music choice (defaults to this if no choice is received)
    if profile.User.music == "basic":
        play_music("Music/Local/sound_test.wav")
    
    
    if profile.User.music == "upbeat":
        play_music("Music/Local/sound_test.wav")
        
    if profile.User.music == "lo-fi":
        play_music("Music/Local/sound_test.wav")
    
        

# NOTE: Create a function that will call on the User class in the profile and play the appropriate music.  