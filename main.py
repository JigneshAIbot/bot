import time
import pyjokes
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import speedtest
import sys
import os
import smtplib
import random
import tkinter as tk
import re
import JarvisAI
import subprocess
from textblob import TextBlob
import geoip2.database
import requests
import pywhatkit as kit
from requests import get
from lsHotword import ls

name = "Jignaass"
obj = JarvisAI.JarvisAssistant()
engine = pyttsx3.init()
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[0].id)

starting = ["Hello!", "Hey!", "How are you?", "How's day going?"]
greetings = ["Your welcome sir!", "Happy to help you sir", "Here for you anytime!"]
goodbyes = ["See you soon!", "Have a great day!", "Good bye", "Bye-Bye", "Cya"]
prefix = ["Hold on,", "Alright,", "Hang on,", "Okay sir,"]


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")
    if 0 <= hour < 12:
        speak(f"Good Morning!, its {tt}")

    elif 12 <= hour < 18:
        speak(f"Good Afternoon!, its {tt}")
    else:
        speak(f"Good Evening! its {tt}")

    start = random.choice(starting)
    speak(f"{start} sir, I am {name} your personal assistant! How may I help you?")


def takeCommand():
    # It takes microphone i/o from the user and return string
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        # print(f"You said: {query.lower()}\n")

    except Exception:
        speak("I couldn't understand it, say that again sir.....")
        print("Say that again please....")
        return "None"
    return query.lower()


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremailid', 'password')
    server.sendmail('youremailid', to, content)
    server.close()


class CurrencyConverter():
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        # first convert it into USD if it is not in USD.
        # because our base currency is USD
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]

        # limiting the precision to 4 decimal places
        amount = round(amount * self.currencies[to_currency], 4)
        return amount


def Tasks():
    global name
    while True:
        query = takeCommand().lower()
        # query = "convert currency"

        if 'morning already' in query:
            hour = int(datetime.datetime.now().hour)
            if 0 <= hour < 12:
                speak("Yes, sir it is " + datetime.datetime.now().strftime("%H and %M") + "Good morning!")

            elif 12 <= hour < 18:
                speak("Nein, sir it is " + datetime.datetime.now().strftime("%H and %M") + "Good Afternoon!")
            else:
                speak("Negative, sir it is " + datetime.datetime.now().strftime("%H and %M") + "Good evening!")
            speak("what is my task for today master!?")

        elif 'convert' in query:
            if 'currency' in query or 'money' in query:
                speak("say initials of which currency you want to convert")
                base = takeCommand().upper()
                # print(base)
                speak("say initials of in which you want to convert")
                con = takeCommand().upper()
                # print(con)
                speak("how much amount you want to convert? sir")
                amount = takeCommand()
                # print(amount)
                url = 'https://api.exchangerate-api.com/v4/latest/USD'
                converter = CurrencyConverter(url)
                conamount = converter.convert(base, con, int(amount))
                # print(conamount)
                speak("After converting the amount is " + str(conamount))

        elif 'calculate' in query:
            speak("Which method you want to calculate in, sir?")
            method = takeCommand().lower()
            # print(method)
            if 'sum' in query or 'addition' in query:
                speak("Say the first value sir!")
                fvalue = float(takeCommand())
                speak("Say the second value sir!")
                svalue = float(takeCommand())
                finalvalue = fvalue + svalue
                speak(f"Sum of {str(fvalue)} + {str(svalue)} is {str(finalvalue)}")
                # print(finalvalue)
            elif 'multiply' in query:
                speak("Say the first value sir!")
                fvalue = float(takeCommand())
                speak("Say the second value sir!")
                svalue = float(takeCommand())
                finalvalue = fvalue * svalue
                speak(f"Multiplication of {str(fvalue)} into {str(svalue)} is {str(finalvalue)}")
                # print(finalvalue)
            elif 'divide' in query or 'division' in query:
                speak("Say the first value sir!")
                fvalue = float(takeCommand())
                speak("Say the second value sir!")
                svalue = float(takeCommand())
                finalvalue = fvalue / svalue
                speak(f"Division of {str(fvalue)} by {str(svalue)} is {str(finalvalue)}")
                # print(finalvalue)
            elif 'subtraction' in query or 'subtract' in query or 'minus' in query:
                speak("Say the first value sir!")
                fvalue = float(takeCommand())
                speak("Say the second value sir!")
                svalue = float(takeCommand())
                finalvalue = fvalue - svalue
                speak(f"By Subtracting {str(fvalue)} from {str(svalue)}, remaining digits is {str(finalvalue)}")
                # print(finalvalue)
            else:
                speak("Sorry I couldn't understand it sir!")

        elif 'translate' in query or 'translator' in query:
            speak("do i need to detect the language or not?")
            ans = takeCommand().lower()
            if ans == 'yes' or 'detect':
                speak("Start speaking to detect!")
                detect = query.lower()
                # detect = 'tumhara name kya hai'
                blob = TextBlob(u'' + detect)
                # print(blob.detect_language())
                speak("Language detected!")
                speak("Translating to english sir.")
                # print(blob.translate(to='en'))
                speak(blob.translate(to='en'))
            elif ans == 'no' or ans == 'don\'t':
                speak("from which language I need to translate from sir?")
                lan = takeCommand().lower()
                # print(lan)
                speak("start speaking to translate!")
                trans = takeCommand().lower()
                blob = TextBlob(u'' + trans)
                speak(blob.translate(to='en'))
            else:
                pass

        # elif 'jarvis' in query:
        #   speak("I am dreamnoid sir, and who is jarvis firstly!")
        #    query = takeCommand().lower()
        #   if 'sorry dreamnoid' in query:
        #       speak("who is jarvis not the sorry sir. you have sidebot")
        #   elif 'my x' in query:
        #       speak("you never had relationship sir, don't lie lol")
        #   else:
        #       "huh! whatever, tell me what to do."
        #   query = takeCommand().lower()
        #  if 'angry' in query:
        #       speak("ohh, ofcourse i am not what you think so.")
        #   else:
        #      speak("Surely! you don't even need to remember my name.")
        #       speak("please tell me again what to do?")
        #       break

        elif 'long day' in query or 'without you' in query:
            speak("Aw! sir, i you missed me sir?")
            query = takeCommand()
            if 'of course' in query or 'yes' in query:
                speak("That's so sweet of you sir. But you should work on your own sometimes!")
            else:
                speak("Ah! i know you miss me but it was a nice day without work i must say! he he he he he he")

        elif 'to follow' in query:
            speak("without a doubt sir!")

        elif 'nothing' in query or 'nothing for right now' in query or 'no work' in query:
            speak("Alright, sir ask me whenever you need.")

        elif 'search online' in query:
            # query = takeCommand()
            if 'about' in query:
                query = query.replace("search online about", "")
            elif 'for' in query:
                query = query.replace("search online for", "")
            elif 'jarvis' in query:
                query = query.replace("search online", "").replace("jarvis", "")
            elif 'dreamnoid' in query:
                query = query.replace("search online", "").replace("dreamnoid", "")
            if 'for' and 'dreamnoid' in query:
                query = query.replace("search online for", "").replace("dreamnoid", "")
            elif 'about' and 'dreamnoid' in query:
                query = query.replace("search online about", "").replace("dreamnoid", "")
            if 'for' and 'jarvis' in query:
                query = query.replace("search online for", "").replace("jarvis", "")
            elif 'about' and 'jarvis' in query:
                query = query.replace("search online about", "").replace("jarvis", "")
            else:
                query = query.replace("search online", "")

            prefixran = random.choice(prefix)
            speak(prefixran + ", I will show you information about " + query + ".")
            chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(chrome_path).open("http://www.google.com/search?q=" + query)
            speak("Here, it is in your screen sir!")

        elif 'my ip address' in query:
            ip = get('https://api.ipify.org').text
            speak(f"Your ip address is {ip} sir.")

        elif 'send message' in query:
            speak("To which number you want to send message sir")
            speak("say the number please")
            number = int(takeCommand())
            speak("What should I write in message sir?")
            msg = takeCommand()
            speak("at what hour i should send message sir?")
            hr = int(takeCommand())
            speak("at what minute sir?")
            mi = int(takeCommand())
            kit.sendwhatmsg(number, msg, hr, mi)
            speak("Message successfully sent sir.")

        elif 'check internet speed' in query or 'internet speed' in query or 'speed of internet' in query:

            st = speedtest.Speedtest()
            st.get_best_server()
            rawdl = st.download()
            roundedspeed = round(rawdl)
            finaldl = format(roundedspeed / 1e+6, ".2f")
            rawup = st.upload()
            roundedspeedup = round(rawup)
            finalup = format(roundedspeedup / 1e+6, ".2f")
            # print(f"We have {finaldl} mega bytes per second downloading speed and {finalup} mega bytes per second uploading speed")
            speak(f"We have {finaldl} mega bytes per second downloading speed and {finalup} mega bytes per second uploading speed")

        elif 'on youtube' in query:
            speak("What should i play")
            topic = takeCommand()
            kit.playonyt(topic)
            prefixran = random.choice(prefix)
            speak(prefixran + ", On to it!")

        elif 'wikipedia' in query:
            speak('Searching wikipedia.......')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            speak(results)

        elif 'your name' in query:
            speak("My name is " + name)

        elif 'play game' in query:
            steamPath = "C:\\Program Files (x86)\\Steam\\Steam.exe"
            os.startfile(steamPath)
            speak('Opening steam sir, Have fun playing!')

        elif 'funny' in query:
            if 'not' in query:
                speak("as if my creator is funny! ha ha ha ha")
            else:
                speak("I know right!")

        elif 'thank you' in query:
            greeting = random.choice(greetings)
            speak(greeting + "")

        elif re.search('launch | open', query):
            dict_app = {
                'chrome': "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                'steam': 'C:\\Program Files (x86)\\Steam\\Steam.exe',
                'discord': 'C:\\Users\\Mavan\\AppData\\Local\\Discord\\app-0.0.309\\Discord.exe',
                'spotify': 'C:\\Users\\Mavan\\OneDrive\\Desktop\\Spotify',
                'pycharm': 'C:\\Program Files\\JetBrains\\PyCharm 2020.2.4\\bin\\pycharm64.exe',
                'CS go': 'C:\\Users\\Mavan\\OneDrive\\Desktop\\Counter-Strike Global Offensive',
                'prompt': 'C:\\Windows\\System32\\cmd'
            }
            keyword_list = ['youtube.com', 'google.com', 'stackoverflow.com', 'CMD']

            word = query.split()
            words = len(word)
            j = 0
            for _ in word:
                if word[j] in keyword_list:
                    prefixran = random.choice(prefix)
                    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
                    webbrowser.get(chrome_path).open(str(word[j]))
                    speak(prefixran + "Starting: " + word[j])
                    pass
                else:
                    j += 1
                if 'cmd' in query:
                    os.system("start cmd")
                    speak("Here it is.")
                    break
                else:
                    for i in range(words):
                        app = query.split(' ', i)[i]
                    '''
                      upper "for" loop for finding the word in the string to open 
                    '''
                    path = dict_app.get(app)
                    if path is None:
                        speak('Application path not found')
                        print('Application path not found')
                        break
                    else:
                        prefixran = random.choice(prefix)
                        speak(prefixran + 'Launching: ' + app)
                        obj.launch_any_app(path_of_app=path)
                        break

        elif 'shutdown' in query:
            if 'pc' in query or 'computer' in query or 'system' in query:
                prefixran = random.choice(prefix)
                speak("Are you sure you want to shutdown sir? say yes if you want cutoff the system.")
                ans = takeCommand().lower()
                if 'yes' in ans:
                    speak(prefixran + " ! Your system is on its way to shut down")
                    subprocess.call('shutdown / p /f')
                else:
                    speak("Command shutdown has been retreated!")
            else:
                pass

        elif "restart" in query:
            if 'pc' in query or 'computer' in query or 'system' in query:
                prefixran = random.choice(prefix)
                speak("Are you sure you want to shutdown sir? say yes if you want cutoff the system.")
                ans = takeCommand().lower()
                if 'yes' in ans:
                    speak(prefixran + " ! Restarting your system, sir!")
                    subprocess.call(["shutdown", "/r"])
                else:
                    speak("Command restart has been retreated!")
            else:
                pass

        elif "don't listen" in query or "stop listening" in query:
            speak("for how much time in seconds you want to stop me from listening sir!")
            a = int(takeCommand())
            speak("I will not be listening for next" + str(a) + "seconds.")
            time.sleep(a)
            # print(a)

        elif re.search('manual | notes | commands', query):
            speak("Showing Notes")
            file = open("jigneshAIbot.txt", "r")
            # print(file.read())
            speak(file.read(6))

        elif 'play music' in query:
            speak('Playing your favourite songs now!')
            music_dir = 'D:\\MUJIC'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'current time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f'Current time is {strTime} sir.')

        elif 'date' in query:
            strDate = datetime.datetime.now().date()
            speak(f'Current date is {strDate} sir.')

        elif 'joke' in query:
            speak(pyjokes.get_joke())

        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                speak('Alright, to whome sir?')
                to = input()
                sendEmail(to, content)
                speak("Email sent successfully")
            except Exception as e:
                # print(e)
                speak("Sorry, I am not able to send this email for some reasons.")

        elif 'trace ip' in query or 'find ip' in query or 'locate ip' in query:
            reader = geoip2.database.Reader('./GeoLite2-City/GeoLite2-City.mmdb')
            try:
                speak("Speak the ip address only sir!")
                ip = takeCommand()
                ip = ip.replace(" ", "")
                # ip = '150.107.241.230'
                response = reader.city(ip)
                speak(str(ip) + "has been traced and details are as follow")
                speak("Country is " + response.country.name)
                speak("postal code is" + response.postal.code)
                speak("in the state of" + response.subdivisions.most_specific.name)
                speak("and" + response.city.name + "is the city name")
                speak("Location in latitude and longitude is")
                speak(str(response.location.latitude) + "and   ")
                speak(str(response.location.longitude) + "Respectively")
            except Exception:
                # print(f"Say that again sir, couldn't trace the ip {ip}.")
                ip = takeCommand()
                return "None"

        elif "change name" in query:
            speak("What would you like to call me, Sir ")
            name = takeCommand()
            speak("Thanks for naming me, sir")

        elif "who made you" in query or "who created you" in query:
            speak("I have been created by Rishit Mavani.")

        elif "where is" in query:
            data = query.split(" ")
            i = len(data)
            location = data[i - 1]
            prefixran = random.choice(prefix)
            speak(prefixran + ", I will show you where " + location + " is.")
            chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(chrome_path).open("http://www.google.com/maps/place/" + location + "/&amp;")
            speak("Here, it is sir.")

        elif 'have sleep' in query or 'neutralize yourself' in query:
            speak("Alright sir, i am going to sleep, awake me anytime when you need sir.")
            break

        def wakeLoop():
            print("say hey jignesh to activate again")
            ls.lsHotword_loop()
            Tasks()

        wakeLoop()


if __name__ == "__main__":
    window = tk.Tk()

    label_1 = tk.Label(text="Username:")
    entry_var = tk.StringVar()
    label_1.pack()
    entry = tk.Entry(window, textvariable=entry_var)
    entry.pack()

    # print(entry_var.get())


    def activate():
        var = entry_var.get()
        if var == '' or None:
            speak("Please enter the name sir this field cannot be empty!")
        else:
            label_1.pack_forget()
            entry.pack_forget()
            button.pack_forget()
            start = random.choice(starting)
            label_name.pack()
            button_1.pack(pady=10)
            speak("Registered as " + var)
            speak(start + "sir, Click button to activate your personal assistant Jiggnnass!")
            # print(f"Registered, as {var}")


    label_name = tk.Label(
        text=f"Hello, This is {name}",
        foreground="white",  # Set the text color to white
        background="black"  # Set the background color to black
    )


    def start():
        while True:
            # print("Say, hey jignesh or ai jignesh")
            ls.lsHotword_loop()
            # query = takeCommand().lower()
            permission = "wake up"
            if 'wake up' in permission or 'hey jignesh' in permission or 'hello jignesh' in permission or 'ai jignesh' in permission:
                wishMe()
                Tasks()
            elif 'quit' in permission or 'have sleep' in permission:
                speak('Auf wiedersehen, Have a great time sir!')
                sys.exit()


    def handle_click():
        window.destroy()
        # print("Activated!")
        speak("Activated")
        speak("Say, hey jignesh to power-up your assistant!")
        start()


    button = tk.Button(
        window,
        text="Click to register!",
        bg="blue",
        fg="yellow",
        command=activate,
    )


    def manual():
        speak("Opening manual!")
        os.startfile("jigneshAIbot.txt.txt")


    button_manual = tk.Button(
        window,
        text='Click to see manual',
        bg="black",
        fg="white",
        command=manual
    )

    button_1 = tk.Button(
        window,
        text="Click to activate!",
        bg="blue",
        fg="yellow",
        command=handle_click,
    )


    def exit1():
        goodbye = random.choice(goodbyes)
        speak(f"Exiting! sir, {goodbye}")
        exit()


    button_exit = tk.Button(
        window,
        text='Quit',
        bg='red',
        fg='black',
        command=exit1,
    )

    button.pack(pady=10)
    button_manual.pack(pady=10)
    button_exit.pack(pady=5)

    window.mainloop()
