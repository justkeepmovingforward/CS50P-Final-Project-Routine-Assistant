import time
import pyttsx3
import speech_recognition as sr
import schedule
import json
import random
import re
from weekly_routine import weekly
from weekly_routine import name
from tabulate import tabulate

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

water_list = []
chore_list = []
water_counter = []
water_sched = "water_sched.json"
chore_sched = "chore_sched.json"

water_reminder_interval=1
daily_reminder_interval=5


username=str(name())

def introduction():
    intro = (f"Hello {username}, my name is CherryPy, your routine assistant."
             "I can help you track your water intake and remind you of"
             "daily and weekly tasks to keep you on track with your goals."
             "just input your tasks,"
             "and I'll take care of the rest."
             "                              "
             "For water intake counter, just type 'water',"
             "                                             "
             ",Don't forget to type start when you're finished."
             "To quickly resume your previous routine, just type  'start',"
             "                                                        "
             "your most recent routine is always saved for easy access")

    introspeech = intro.split(".")
    for i in introspeech:
        engine.say(i)
        engine.runAndWait()
        time.sleep(0.000001)

def main():
    skip_intro=input("need introduction/instructions? yes/no? ")
    if skip_intro=="yes":
        introduction()
    elif skip_intro=="no":
        pass
    else:
        engine.say("I'm taking that as a no")
        engine.runAndWait()
        pass
    engine.say(f"kindly input your routine now.,")
    engine.runAndWait()
    print("\nsample:\n"
          "7:00am water (for water intake tracker)\n"
          "7:30am breakfast\n"
          "'start' when done\n")
    routine_input()

def routine_input():
    while True:
        task_input=validation()
        try:
            if "start" in task_input:
                running()
        except TypeError:
            #print("TypeError in routine_input")
            continue
        else:
            hr,minn,ampm,task=task_input
            #print(hr,minn,ampm)
            newtime=convert_to_24hour(hr,minn,ampm)
            #print("ctime",ctime)
        try:
            recording(task,newtime)
        except (TypeError,UnboundLocalError):
            #print("error in routine_input except")
            continue


def validation():
    try:
        task_input = input("daily routine: ")
        if pattern := re.match(
                r"^[ ]*(?P<hour>[0-9]?[0-9])[ ]*:[ ]*(?P<minutes>[0-5][0-9])[ ]*(?P<ampm>AM|PM)[ ]*"
                r"[-:/\|;,~_+=!@#$%^&*(){}`<>]*[ ]*(?P<task>.+)$",
                task_input, re.IGNORECASE):
            hr = int(pattern.group("hour"))
            minn = int(pattern.group("minutes"))
            ampm = str(pattern.group("ampm")).upper()
            task = str(pattern.group("task")).lower()
            if task.startswith("am ")or task.startswith("pm ") or task.startswith("pm"):
                raise TypeError
            else:
                #print("validation","hr:",hr,"min:",minn,"ampm:",ampm,"task:",task)
                return hr,minn,ampm,task
        elif task_input=="start":
            return "start"
        else:
            #print("wrong input in validation func")
            print("invalid input")
            engine.say(f"kindly review the proper format")
            engine.runAndWait()
            pass

    except TypeError:
        #print("error in validation except TypeError")
        print("invalid time marker")
        engine.say(f"check your time marker")
        engine.runAndWait()
        pass
    except Exception:
        #print("error in validation exception")
        print("invalid input")
        engine.say(f"kindly review the proper format")
        engine.runAndWait()
        pass


def convert_to_24hour(hr,minn,ampm):
    try:
        hr=int(hr)
        minn=int(minn)
        ampm=ampm.upper()
        if hr==00:
            raise ValueError
        elif hr > 12:
            raise ValueError
            pass
        elif minn > 59:
            raise ValueError
            pass
        elif hr < 12 and ampm == "PM" and minn < 60:
            hr += 12
        elif hr == 12 and ampm == "AM":
            hr = 00
        elif hr == 12 and ampm == "PM":
            hr = 12
        elif ampm=="AMPM":
            raise ValueError
        #print("before ctime var", hr, minn, ampm)
        ctime = f"{hr:02d}:{minn:02d}"
        return ctime
    except (ValueError):
        print("not in 12-hour format")
        engine.say("use 12-hour format")
        engine.runAndWait()
        pass

def recording(task,newtime):
    newtime2=newtime
    task2=task
    chore = task2.lstrip()

    if "water" in chore.lower():
        water_list.append({"Time": newtime2, "Chore": chore})
        with open(water_sched, 'w') as sched:
            json.dump(water_list, sched, indent=4)
            engine.say("recorded")
            engine.runAndWait()
    else:
        chore_list.append({"Time": newtime2, "Chore": chore})
        with open(chore_sched, 'w') as sched:
            json.dump(chore_list, sched, indent=4)
            engine.say("recorded")
            engine.runAndWait()


def running():
    what_to_run=[]
    try:
        try:
            writing_water()
        except FileNotFoundError:
            what_to_run.append("1")
            print("no water reminders found")
            pass

        try:
            writing_chore()
        except FileNotFoundError:
            what_to_run.append("1")
            print("no daily tasks found")
            pass

        if len(what_to_run)<2:
            print("daily routine recorded.")
            engine.say("I've noted your daily routine.")
            engine.runAndWait()

        elif len(what_to_run)==2:
            raise FileNotFoundError

    except FileNotFoundError:
        print("Proceeding without your daily routine reminders.")
        engine.say("You typed start right away, but it seems there’s no previous daily routine recorded yet.\n"
              "Proceeding without your daily routine reminders.")
        engine.runAndWait()
        pass

    verses()
    weekly()
    while True:
        schedule.run_pending()


def writing_water():
    with open(water_sched, 'r') as file:
        water = json.load(file)
    merged_water_dict = {}
    for item in water:
        merged_water_dict[item["Time"]] = item["Chore"]
    water_times = list(merged_water_dict.keys())
    water_chore = list(merged_water_dict.values())
    water_speech(water_times, water_chore)


def water_speech(water_times, water_chore):
    print()
    tabulated=(tabulate({"reminder times":water_times},headers=["water reminder:"]))
    print(tabulated)
    for i, y in zip(water_times, water_chore):
        i = str(i)
        speechwater1 = f"{username} it's {i}, time for drinking {y} "

        def water_speak(speechwater2=speechwater1):
            engine.say(speechwater2)
            engine.runAndWait()
        try:
            schedule.every().day.at(i).do(water_speak)
        except Exception:
            pass
        try:
            hr, mmin = i.split(":")
            hr = int(hr)
            mmin = int(mmin)
            minutes = mmin + water_reminder_interval
            if minutes >= 60:
                hr = hr + 1
                minutes = minutes - 60
                if hr==24:
                    hr=00

            reminder_time = f"{hr:02d}:{minutes:02d}"
        except ValueError:
            print("water speech error")
            pass

        def repeater():
            engine.say(f"Hi {username}, have you drank 1 glass of water?")
            engine.runAndWait()
            water_intake_counter()
        try:
            schedule.every().day.at(reminder_time).do(repeater)
        except Exception:
            print("problem with water repeater")
            pass


def water_intake_counter():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = ""
        try:
            audio = recognizer.listen(source, timeout=10)
            audio = recognizer.listen(source)
            recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception:
            print("No speech detected within the timeout period.")
            pass

    try:
        response = recognizer.recognize_sphinx(audio).lower()

        if "yes" in response:
            water_counter.append("1")
            wl = len(water_counter)
            print("water intake:",wl,"glass/es")
            answer = f"That's good {username}! you have now drank a total of {wl} glasses"
        else:
            answer = f"Please drink now {username}. You need 8 glasses of water everyday so you won't get sick"

        engine.say(answer)
        engine.runAndWait()

    except Exception:
        engine.say("Kindly plug in a microphone if you'd like me to track your water intake.")
        engine.runAndWait()
        pass


def writing_chore():
    with open(chore_sched, 'r') as file:
        chores = json.load(file)

    merged_chores_dict = {}
    for item in chores:
        merged_chores_dict[item["Time"]] = item["Chore"]
    chore_times = list(merged_chores_dict.keys())
    chore_chore = list(merged_chores_dict.values())
    print(tabulate({"Time":chore_times,"Task":chore_chore},headers="keys",tablefmt="psql"))
    chore_speech(chore_times, chore_chore)


def chore_speak(chore_speech2):
    engine.say(chore_speech2)
    engine.runAndWait()


def repeater2(username, task):
    engine.say(f"Hi {username}, I'd like to remind you of the task {task}.")
    engine.runAndWait()


def chore_speech(chore_times, chore_chore):
    for s, t in zip(chore_times, chore_chore):
        s = str(s)
        chore_speech1 = f"It's {s}, time to {t} "
        try:
            schedule.every().day.at(s).do(chore_speak, chore_speech1)
        except Exception:
            pass
        try:
            hr2, min2 = s.split(":")
            hr2 = int(hr2)
            min2 = int(min2)
            minutes2 = min2 + daily_reminder_interval
            if minutes2 >= 60:
                hr2 = hr2 + 1
                minutes2 = minutes2 - 60
                if hr2==24:
                    hr2=00
            reminder_time2 = f"{hr2:02d}:{minutes2:02d}"
        except Exception:
            pass
        try:
            schedule.every().day.at(reminder_time2).do(repeater2, username, t)
            #time.sleep(1)
        except Exception:
            print("problem with chore repeater")
            pass

def inspire():
    with open("verses.csv", "r", newline="") as verse:
        reader=verse.readlines()
        total_entries=len(reader)
        r=random.randint(1,total_entries-1)
        quotes=reader[r]
        print(quotes)
        engine.say(f"Here's a message for you {username}")
        engine.runAndWait()
        engine.say(quotes)
        engine.runAndWait()

def verses():
        schedule.every(3).hours.at("07:00").do(inspire)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt,RuntimeError):
        print("You stopped the program.")
        engine.say("Deactivating")
        engine.runAndWait()
