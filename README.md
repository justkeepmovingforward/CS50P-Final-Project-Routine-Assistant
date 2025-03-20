
# Routine Assistant

Welcome to my CS50 final project! I've developed a unique routine assistant program designed to help you stay on track with your daily tasks. Unlike typical assistants that only send reminders, my program goes a step further – it speaks to you, gently guiding you through your routines and encouraging you to complete them.

One of the key features is the water intake tracker, which counts how many times you say "yes" throughout the day, helping you monitor your hydration. This program turns everyday tasks into interactive moments, reinforcing good habits, especially for busy parents who often forget to take care of themselves.

## Features

- Tracks daily water intake
- Provides daily and weekly routine reminders
- Reminders are delivered via spoken audio, not displayed on screen
- Randomly speaks inspirational messages or Bible verses
- Personalizes the experience by addressing the user by name
- Runs seamlessly in the background
- Functions offline, without requiring an internet connection
- Allows for one-time input of routine details


## Description

This program consists of two Python files: `project.py` and `weekly_routine.py`.

- `project.py` serves as the main entry point and imports functions from `weekly_routine.py`.
- `weekly_routine.py` contains functions for managing weekly tasks. While these tasks are similar, they cannot be easily handled using object-oriented programming (OOP) due to limitations with the `schedule` module, which does not support passing variables (such as the "day") dynamically.

### project.py

-This is the main file of the program. At the top, I define global variables for easy access, including lists for tracking water intake, chores, and the water counter. It also includes variables for file management.

-The water intake and chore/task intervals are specified here, allowing the user to manually set the time between each routine reminder.

#### username' variable

-This value is obtained by calling the `name()` function from `weekly_routine.py`, where the input for the `username` variable is requested from the user and then returned by the `name()` function.

#### main

-The program prompts the user to decide whether they want to hear an introduction, which includes instructions. If the user responds with 'yes', the introduction() function is called. If the answer is 'no' or anything other than 'yes', the program simply continues without showing the introduction. A sample input will be provided for clarity.

#### introduction

-During the introduction, the program will address the user by the name they provided and deliver the instructions using the `pyttsx3` library to speak them aloud.

#### routine_input

-Regardless of whether the user wants an introduction or not, the program will continue prompting for the user's routine. The input process ends when the user types "start." This function also triggers other functions to process the provided input.

#### validation

-This is the first function called by routine_input(). Here, inputs are filtered using a regex pattern. Valid inputs, which consist of an hour, colon, minutes (and optional special characters), along with the task, are validated. Inputs that don't meet these criteria will raise an exception, and a corresponding message will be spoken by `pyttsx3`. Once validated, the input is returned back to `routine_input` for further processing.

#### convert_to_24hour

-The validated input is then broken down into several variables: `hr` (hour), `minn` (minutes), `ampm` (time marker), and `task`. The hour, minutes, and time marker are passed to this function, while the `task` variable remains in `routine_input` as it is not needed here. The 12-hour format is then converted into a 24-hour format using conditionals. The function returns the time as a string in 24-hour format, now without the time marker, and stores it in the `newtime` variable in routine input().

#### recording

-The `newtime` and `task` from `routine_input` are then passed to this function to determine whether they should be stored in the water or chore JSON file. These daily tasks must be stored in separate JSON files to ensure the water tracker functions correctly. For each valid input, the word "recorded" is passed to `pyttsx3` to confirm the task has been successfully logged.


#### running

-Once the user types "start," this function is called, signaling the end of routine input. Inside this function, a list variable is used to hold the values for each of the files, either the water or chore JSON file. Before calling each file, I append a value to the list to handle the conditional logic that ensures the program continues running even if one of the files is missing. For example, if the user has only provided details for the water intake tracker or vice versa, this conditional approach effectively handles the "file not found" error, allowing the program to function even if one of the files is absent.

#### writing_water

-The JSON file for the water tracker is opened and processed, converting it from a dictionary into separate lists. These lists are then passed to the `water_speech` function for further processing.

#### water_speech

-Water tracker details are displayed using the `tabulate` module. The scheduling for water reminders is set by iterating over the time list. In this script, `i` represents the time values, and `y` is used for the water reminders.
Here is the script:


    f"{username} it's {i}, time for drinking {y} "

-Each reminder runs twice, and the interval between them can be set at the beginning of the code in a list called `water_reminder_interval`. The `i` (time) is broken down into different variables that store the integer version of the time, allowing the addition of the `water_reminder_interval`. The hour and minutes in 24-hour format are then converted back into a string, which is used in another schedule to run the second round of reminders.

this is what pyttsx3 will say the second time:

    f"Hi {username}, have you drank 1 glass of water?"

#### water_intake_tracker

-This function is called after the second round of speech in the `water_speech` function. It utilizes speech recognition to listen for and count every "yes" the user says. The function also handles errors, such as when the microphone is absent, when the user says something other than "yes," or if there is an issue with the speech recognition module.

#### writing_chore and chore_speech

-These functions are similar to `writing_water` and `water_speech`, but they process a different file, and there is no need for speech recognition. However, the schedule still runs twice, and the interval between them can also be set in a list at the beginning of the code, which is stored in the `chore_reminder_interval` variable.

#### `inspire()` and `verses()`

-The `inspire()` function selects a random quote from the `verses.csv` file and reads it aloud using `pyttsx3`, addressing the user by name.

-The `verses()` function schedules the `inspire()` function to run every 3 hours starting at 7:00 AM, providing periodic inspirational reminders.

#### weekly

-this function is imported from the weekly_routine module


### weekly_routine.py

#### name

-This function stores and returns the value from the `username` input, which will then be exported to the `project.py` file.

#### weekly

-All other functions of this module are embedded in this function. It first asks the user if they want to set weekly routines. If the answer is "yes," the function will proceed to ask for input. If the answer is "no," the `no_weekly()` function will be called.

##### no_weekly

-The `no_weekly()` function is called when the user decides not to set a weekly routine. It prints "no weekly routine" and uses `pyttsx3` to speak a message confirming that only daily routines will be set and the CherryPy app will be activated.

##### Main

-A "yes" response will call the `Main()` function. In this function, the program asks for user input in the same format as the validation function in `project.py`. It works similarly to `project.py`, but this function handles sorting tasks into 7 different days, requiring 7 separate JSON files—one for each day.

##### running_weekly

-In this function, I used the same logic as the running function in `project.py` to handle `FileNotFoundError`. I created a list to store the values appended to each file, allowing the program to continue running even if only one of the 7 days has routine input.



## Demo


https://www.youtube.com/watch?v=I9cXI8plcBw
## Authors

- [Cherry Ho](https://www.github.com/justkeepmovingforward)
