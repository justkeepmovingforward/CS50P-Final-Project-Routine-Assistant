import time
from datetime import datetime
import pyttsx3
import schedule
import json
import re
from tabulate import tabulate

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

sunday_list = []
monday_list = []
tuesday_list = []
wednesday_list = []
thursday_list = []
friday_list = []
saturday_list = []

weekly_reminder_interval=1

username = input("What is your name? ")


def name():
    passed_name = str(username)
    return passed_name


def weekly():
    def Main():
        while True:
            task_input = input("weekly routine: ")
            if task_input.lower() == "start":
                break
            if pattern := re.match(
                    r"^[ ]*(?P<days>Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)[ ]*(?P<hour>[0-9]?[0-9])[ ]*\:"
                    r"[ ]*?(?P<minutes>[0-5][0-9])[ ]*(?P<ampm>AM|PM)[ ]*[-:/\|;,~_+=!@#$%^&*(){}`<>]*[ ]*(?P<task>.+)$",
                    task_input, re.IGNORECASE):

                days = str(pattern.group("days"))
                hr = int(pattern.group("hour"))
                minn = int(pattern.group("minutes"))
                ampm = str(pattern.group("ampm")).upper()
                task = str(pattern.group("task"))
                try:
                    if hr > 12:
                        raise ValueError
                        pass
                    elif minn > 59:
                        raise ValueError
                        pass
                    if hr < 12 and ampm == "PM" and minn < 60:
                        hr += 12
                    elif hr == 12 and ampm == "AM":
                        hr = 00
                    elif hr == 12 and ampm == "PM":
                        hr = 12

                except ValueError:
                    print("invalid time format")
                    engine.say(f"Invalid time format")
                    engine.runAndWait()
                    pass

                try:
                    ctime = f"{hr:02d}:{minn:02d} {ampm}"
                    ntime = datetime.strptime(ctime, '%H:%M %p')
                    newtime = datetime.strftime(ntime, '%H:%M')
                except ValueError:
                    print("valuerror")
                    pass

                chore = task.lstrip()
                try:
                    if days == "sun" or days == "sunday":
                        sunday_list.append({"Time": newtime, "Chore": chore})
                        with open("sunday.json", 'w') as sched:
                            json.dump(sunday_list, sched, indent=4)

                    elif days == "mon" or days == "monday":
                        monday_list.append({"Time": newtime, "Chore": chore})
                        with open("monday.json", 'w') as sched:
                            json.dump(monday_list, sched, indent=4)

                    elif days == "tues" or days == "tuesday":
                        tuesday_list.append({"Time": newtime, "Chore": chore})
                        with open("tuesday.json", 'w') as sched:
                            json.dump(tuesday_list, sched, indent=4)

                    elif days == "wed" or days == "wednesday":
                        wednesday_list.append({"Time": newtime, "Chore": chore})
                        with open("wednesday.json", 'w') as sched:
                            json.dump(wednesday_list, sched, indent=4)

                    elif days == "thurs" or days == "thursday":
                        thursday_list.append({"Time": newtime, "Chore": chore})
                        with open("thursday.json", 'w') as sched:
                            json.dump(thursday_list, sched, indent=4)

                    elif days == "fri" or days == "friday":
                        friday_list.append({"Time": newtime, "Chore": chore})
                        with open("friday.json", 'w') as sched:
                            json.dump(friday_list, sched, indent=4)

                    elif days == "sat" or days == "saturday":
                        saturday_list.append({"Time": newtime, "Chore": chore})
                        with open("saturday.json", 'w') as sched:
                            json.dump(saturday_list, sched, indent=4)
                except Exception:
                    print("problem with writing on files")
                    pass
            else:
                print("wrong input format")
                engine.say(f"kindly review the proper format")
                engine.runAndWait()
                pass

        running_weekly()

    def running_weekly():
        with_sched=[]
        try:
            try:
                Sun()
            except FileNotFoundError:
                with_sched.append("1")
                pass
            try:
                Mon()
            except FileNotFoundError:
                with_sched.append("1")
                pass
            try:
                Tues()
            except FileNotFoundError:
                with_sched.append("1")
                pass
            try:
                Wed()
            except FileNotFoundError:
                with_sched.append("1")
                pass
            try:
                Thurs()
            except FileNotFoundError:
                with_sched.append("1")
                pass
            try:
                Fri()
            except FileNotFoundError:
                with_sched.append("1")
                pass
            try:
                Sat()
            except FileNotFoundError:
                with_sched.append("1")
                pass


            if len(with_sched)<7:
                print("weekly routine recorded.")
                print()
                engine.say("I've noted your weekly routine."
                            f"...........,,,,,,,,,,,,,,,,,,"
                            f"activating CherryPy app now")
                engine.runAndWait()
            elif len(with_sched)==7:
                raise FileNotFoundError
                pass
        except FileNotFoundError:
            print("No weekly routine found\n"
                    "Proceeding with:\n"
                    "1. just daily routine reminders(if any)\n"
                    "2. inspirational messages.\n")
            engine.say("You typed 'start' right away, but it looks like no weekly routine is recorded yet.\n"
                       "Feel free to restart the app and add weekly inputs for reminders, or I can continue without them,"
                       "                                ,"
                       "For now, only daily reminders and inspirational messages will run. "
                       "Activating CherryPy app now.")
            engine.runAndWait()
        while True:
            schedule.run_pending()
            time.sleep(1)

    def Sun():
        def writing_sun():
            with open("sunday.json", 'r') as file:
                week = json.load(file)

            weeklist = {}
            for item in week:
                weeklist[item["Time"]] = item["Chore"]
            new_weeklist = [weeklist]
            weekly_dict = new_weeklist[0]
            week_times = list(weekly_dict.keys())
            week_chore = list(weekly_dict.values())
            print("---")
            print(tabulate({"Time": week_times, "Task": week_chore}, headers=["Sunday"], tablefmt="rst"))
            week_speech(week_times, week_chore)

        def week_speak(weekly_speech2):
            engine.say(weekly_speech2)
            engine.runAndWait()

        def sunrepeater(username, task):
            engine.say(f"Hi {username}, I'd like to remind you of your Sunday task {task}.")
            engine.runAndWait()

        def week_speech(chore_times, chore_chore):
            for s, t in zip(chore_times, chore_chore):
                s = str(s)
                weekly_speech1 = f"It's {s}, time to {t} "
                try:
                    schedule.every().sunday.at(s).do(week_speak, weekly_speech1)
                except Exception:
                    pass
                try:
                    hr2, min2 = s.split(":")
                    hr2 = int(hr2)
                    min2 = int(min2)
                    minutes2 = min2 + weekly_reminder_interval
                    if minutes2 >= 60:
                        hr2 = hr2 + 1
                        minutes2 = minutes2 - 60
                        if hr2 == 24:
                            hr2 = 00
                    reminder_time2 = f"{hr2:02d}:{minutes2:02d}"
                    # print("sunday reminder:", reminder_time2)
                except ValueError:
                    pass
                try:
                    schedule.every().sunday.at(reminder_time2).do(sunrepeater, username, t)
                    time.sleep(1)
                except Exception:
                    print("problem with sunday repeater")
                    pass

        writing_sun()

    def Mon():

        def writing_mon():
            with open("monday.json", 'r') as file:
                week = json.load(file)

            weeklist = {}
            for item in week:
                weeklist[item["Time"]] = item["Chore"]
            new_weeklist = [weeklist]
            weekly_dict = new_weeklist[0]
            week_times = list(weekly_dict.keys())
            week_chore = list(weekly_dict.values())
            print("---")
            print(tabulate({"Time": week_times, "Task": week_chore}, headers=["Monday"], tablefmt="rst"))
            week_speech(week_times, week_chore)

        def week_speak(weekly_speech2):
            engine.say(weekly_speech2)
            engine.runAndWait()

        def monrepeater(username, task):
            engine.say(f"Hi {username}, I'd like to remind you of your Monday task {task}.")
            engine.runAndWait()

        def week_speech(chore_times, chore_chore):
            for s, t in zip(chore_times, chore_chore):
                s = str(s)
                weekly_speech1 = f"It's {s}, time to {t} "
                try:
                    schedule.every().monday.at(s).do(week_speak, weekly_speech1)
                except Exception:
                    pass
                try:
                    hr2, min2 = s.split(":")
                    hr2 = int(hr2)
                    min2 = int(min2)
                    minutes2 = min2 + 2
                    if minutes2 >= 60:
                        hr2 = hr2 + 1
                        minutes2 = minutes2 - 60
                        if hr2 == 24:
                            hr2 = 00
                    reminder_time2 = f"{hr2:02d}:{minutes2:02d}"
                    # print("monday reminder:", reminder_time2)
                except ValueError:
                    pass
                try:
                    schedule.every().monday.at(reminder_time2).do(monrepeater, username, t)
                    time.sleep(1)
                except Exception:
                    print("problem with monday repeater")
                    pass

        writing_mon()

    def Tues():
        def writing_tues():
            with open("tuesday.json", 'r') as file:
                week = json.load(file)

            weeklist = {}
            for item in week:
                weeklist[item["Time"]] = item["Chore"]
            new_weeklist = [weeklist]
            weekly_dict = new_weeklist[0]
            week_times = list(weekly_dict.keys())
            week_chore = list(weekly_dict.values())
            print("---")
            print(tabulate({"Time": week_times, "Task": week_chore}, headers=["Tuesday"], tablefmt="rst"))
            week_speech(week_times, week_chore)

        def week_speak(weekly_speech2):
            engine.say(weekly_speech2)
            engine.runAndWait()

        def tuesrepeater(username, task):
            engine.say(f"Hi {username}, I'd like to remind you of your Tuesday task {task}.")
            engine.runAndWait()

        def week_speech(chore_times, chore_chore):
            for s, t in zip(chore_times, chore_chore):
                s = str(s)
                weekly_speech1 = f"It's {s}, time to {t} "
                try:
                    schedule.every().tuesday.at(s).do(week_speak, weekly_speech1)
                except Exception:
                    pass
                try:
                    hr2, min2 = s.split(":")
                    hr2 = int(hr2)
                    min2 = int(min2)
                    minutes2 = min2 + 2
                    if minutes2 >= 60:
                        hr2 = hr2 + 1
                        minutes2 = minutes2 - 60
                        if hr2 == 24:
                            hr2 = 00
                    reminder_time2 = f"{hr2:02d}:{minutes2:02d}"
                    # print("tuesday reminder", reminder_time2)
                except ValueError:
                    pass
                try:
                    schedule.every().tuesday.at(reminder_time2).do(tuesrepeater, username, t)
                    time.sleep(1)
                except Exception:
                    print("problem with tuesday repeater")
                    pass

        writing_tues()

    def Wed():

        def writing_wed():
            with open("wednesday.json", 'r') as file:
                week = json.load(file)

            weeklist = {}
            for item in week:
                weeklist[item["Time"]] = item["Chore"]
            new_weeklist = [weeklist]
            weekly_dict = new_weeklist[0]
            week_times = list(weekly_dict.keys())
            week_chore = list(weekly_dict.values())
            print("---")
            print(tabulate({"Time": week_times, "Task": week_chore}, headers=["Wednesday"], tablefmt="rst"))
            week_speech(week_times, week_chore)

        def week_speak(weekly_speech2):
            engine.say(weekly_speech2)
            engine.runAndWait()

        def wedrepeater(username, task):
            engine.say(f"Hi {username}, I'd like to remind you of your Wednesday task {task}.")
            engine.runAndWait()

        def week_speech(chore_times, chore_chore):
            for s, t in zip(chore_times, chore_chore):
                s = str(s)
                weekly_speech1 = f"It's {s}, time to {t} "
                try:
                    schedule.every().wednesday.at(s).do(week_speak, weekly_speech1)
                except Exception:
                    pass
                try:
                    hr2, min2 = s.split(":")
                    hr2 = int(hr2)
                    min2 = int(min2)
                    minutes2 = min2 + 2
                    if minutes2 >= 60:
                        hr2 = hr2 + 1
                        minutes2 = minutes2 - 60
                        if hr2 == 24:
                            hr2 = 00
                    reminder_time2 = f"{hr2:02d}:{minutes2:02d}"
                    # print("wednesday reminder:", reminder_time2)
                except ValueError:
                    pass
                try:
                    schedule.every().wednesday.at(reminder_time2).do(wedrepeater, username, t)
                    time.sleep(1)
                except Exception:
                    print("problem with Wednesday repeater")
                    pass

        writing_wed()

    def Thurs():

        def writing_thurs():
            with open("thursday.json", 'r') as file:
                week = json.load(file)

            weeklist = {}
            for item in week:
                weeklist[item["Time"]] = item["Chore"]
            new_weeklist = [weeklist]
            weekly_dict = new_weeklist[0]
            week_times = list(weekly_dict.keys())
            week_chore = list(weekly_dict.values())
            print("---")
            print(tabulate({"Time": week_times, "Task": week_chore}, headers=["Thursday"], tablefmt="rst"))
            week_speech(week_times, week_chore)

        def week_speak(weekly_speech2):
            engine.say(weekly_speech2)
            engine.runAndWait()

        def thursrepeater(username, task):
            engine.say(f"Hi {username}, I'd like to remind you of your Thursday task {task}.")
            engine.runAndWait()

        def week_speech(chore_times, chore_chore):
            for s, t in zip(chore_times, chore_chore):
                s = str(s)
                weekly_speech1 = f"It's {s}, time to {t} "
                try:
                    schedule.every().thursday.at(s).do(week_speak, weekly_speech1)
                except Exception:
                    pass
                try:
                    hr2, min2 = s.split(":")
                    hr2 = int(hr2)
                    min2 = int(min2)
                    minutes2 = min2 + 2
                    if minutes2 >= 60:
                        hr2 = hr2 + 1
                        minutes2 = minutes2 - 60
                        if hr2 == 24:
                            hr2 = 00
                    reminder_time2 = f"{hr2:02d}:{minutes2:02d}"
                    # print("thursday reminder:", reminder_time2)
                except ValueError:
                    pass
                try:
                    schedule.every().thursday.at(reminder_time2).do(thursrepeater, username, t)
                    time.sleep(1)
                except Exception:
                    print("problem with thursday repeater")
                    pass

        writing_thurs()

    def Fri():

        def writing_fri():
            with open("friday.json", 'r') as file:
                week = json.load(file)

            weeklist = {}
            for item in week:
                weeklist[item["Time"]] = item["Chore"]
            new_weeklist = [weeklist]
            weekly_dict = new_weeklist[0]
            week_times = list(weekly_dict.keys())
            week_chore = list(weekly_dict.values())
            print("---")
            print(tabulate({"Time": week_times, "Task": week_chore}, headers=["Friday"], tablefmt="rst"))
            week_speech(week_times, week_chore)

        def week_speak(weekly_speech2):
            engine.say(weekly_speech2)
            engine.runAndWait()

        def frirepeater(username, task):
            engine.say(f"Hi {username}, I'd like to remind you of your Friday task {task}.")
            engine.runAndWait()

        def week_speech(chore_times, chore_chore):
            for s, t in zip(chore_times, chore_chore):
                s = str(s)
                weekly_speech1 = f"It's {s}, time to {t} "
                try:
                    schedule.every().friday.at(s).do(week_speak, weekly_speech1)
                except Exception:
                    pass
                try:
                    hr2, min2 = s.split(":")
                    hr2 = int(hr2)
                    min2 = int(min2)
                    minutes2 = min2 + 2
                    if minutes2 >= 60:
                        hr2 = hr2 + 1
                        minutes2 = minutes2 - 60
                        if hr2 == 24:
                            hr2 = 00
                    reminder_time2 = f"{hr2:02d}:{minutes2:02d}"
                    # print("friday reminder:", reminder_time2)
                except ValueError:
                    pass
                try:
                    schedule.every().friday.at(reminder_time2).do(frirepeater, username, t)
                    time.sleep(1)
                except Exception:
                    print("problem with friday repeater")
                    pass

        writing_fri()

    def Sat():

        def writing_sat():
            with open("saturday.json", 'r') as file:
                week = json.load(file)

            weeklist = {}
            for item in week:
                weeklist[item["Time"]] = item["Chore"]
            new_weeklist = [weeklist]
            weekly_dict = new_weeklist[0]
            week_times = list(weekly_dict.keys())
            week_chore = list(weekly_dict.values())
            print("---")
            print(tabulate({"Time": week_times, "Task": week_chore}, headers=["Saturday"], tablefmt="rst"))
            week_speech(week_times, week_chore)

        def week_speak(weekly_speech2):
            engine.say(weekly_speech2)
            engine.runAndWait()

        def satrepeater(username, task):
            engine.say(f"Hi {username}, I'd like to remind you of your Saturday task {task}.")
            engine.runAndWait()

        def week_speech(chore_times, chore_chore):
            for s, t in zip(chore_times, chore_chore):
                s = str(s)
                weekly_speech1 = f"It's {s}, time to {t} "
                try:
                    schedule.every().saturday.at(s).do(week_speak, weekly_speech1)
                except Exception:
                    pass
                try:
                    hr2, min2 = s.split(":")
                    hr2 = int(hr2)
                    min2 = int(min2)
                    minutes2 = min2 + 2
                    if minutes2 >= 60:
                        hr2 = hr2 + 1
                        minutes2 = minutes2 - 60
                        if hr2 == 24:
                            hr2 = 00
                    reminder_time2 = f"{hr2:02d}:{minutes2:02d}"
                    # print("saturday reminder:", reminder_time2)
                except ValueError:
                    pass
                try:
                    schedule.every().saturday.at(reminder_time2).do(satrepeater, username, t)
                    time.sleep(1)
                except Exception:
                    print("problem with saturday repeater")
                    pass

        writing_sat()

    def no_weekly():
        print("no weekly routine")
        engine.say(f"Okay, I will only remind you of your daily routine."
                   f"...........,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"
                   f"activating CherryPy app now")
        engine.runAndWait()

    while True:
        print("\nDo you want to run weekly routine reminders as well?")
        engine.say(f"Do you want to run weekly routine reminders as well? ")
        engine.runAndWait()
        user_weekly = input().lower()

        if user_weekly == "yes":
            print("sample:\n"
                  "monday 8:00am eat breakfast\n"
                  "'start' when done\n")
            engine.say(f"Do not forget to write the day.")
            engine.runAndWait()
            Main()

        elif user_weekly == "no":
            no_weekly()
            break

        else:
            print("kindly type  yes or no")
            engine.say("kindly type  yes or no")
            engine.runAndWait()


if __name__ == "__weekly__":
    weekly()
