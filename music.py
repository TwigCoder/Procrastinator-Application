# Contributors: Krish ##

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
    # Music should loop and not end automatically.
    # It should stop / start playing music when there is a change.
    # You need to find more music files and add them.
        # Divide the locals folder into more folders. One of the folders must be Default.
    # Create a folder in Music called UserMusic (next to Local, NOT in local.)
        # If User wants to play their music, that option will be USERMUSIC in their profile prefernences.
#### DO NOT DELETE THIS ANYONE ####

            


# Define a function to play music
# File-types: MP3, WAV, AIFF

#NOTE: Create a function that takes in a file name (music) as an argument.

# Imports
import multiprocessing
import playsound
import profile
import csv_data
from playsound import playsound



# Creates a function to start the music.
def play_music(file_name):
    
    # Whenever called, will load the playsound command for any file we want.
    p = multiprocessing.Process(target = playsound, args = (file_name,))
    p.start

# Creates a function to stop the music.
def stop_music(file_name):
    
    # Whenever called, will stop the above playsound command.
    p = multiprocessing.Process(target = playsound, args = (file_name,))
    p.terminate


    


# Plays a file based on user's choosing.



    # When called when the timer starts running, plays a specific type of music based on the user's choosing.

# Declares and initialises the variable with the default sound.
userMChoice = "Music/Local/sound_test.wav"

def userMusicChoice():
    
    match profile.user.music:
        
        # If the user does not choose an option or chooses the default option, play the default music.
        case "basic":
            userMChoice = "Music/Local/sound_test.wav"
                
        # If the user chooses the option "lo-fi", play the "lo-fi" music.
        case "lo-fi":
            userMChoice = "Music/Local/sound_test.wav"
        
        # If the user chooses the option "upbeat", play the "upbeat" music.
        case "upbeat":
            userMChoice = "Music/Local/sound_test.wav"
            
    
# Creates a function to check whether to play the music or not, assigned to "music_play".

music_play = csv_data.pull_csv_data('vals.csv', 0, "music" , 1)


# Infinite loop to constantly run the program:
def checkMusicTrue():
    while True:
    music_play = csv_data.pull_csv_data('vals.csv', 0, "music" , 1)
    
    match music_play:
        case 't' :
            music_play = True
        case 'f' :
            music_play = False
    
    #Checks if music_play is true to play the value.
    if music_play == True:
        play_music(userMChoice) 
    else:
        stop_music(userMChoice)