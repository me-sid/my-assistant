from tkinter import *
import PIL
import speech_recognition as rec
import pywhatkit
import datetime
import wikipedia
import pyjokes
from gtts import gTTS
import tenorpy
import webbrowser
import playsound
import urllib
import random
import string
import pyttsx3
import os


def remove_temp():
    for file in os.scandir("temp"):
        os.remove(file.path)


def random_str():
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(5))
    result_str = result_str + ".mp3"
    return result_str


help_command = "Play ... => to play some media\nTell me the time => For current time\n" \
               "tell me a joke => For joke(mainly programming)\nShow me something funny => For funny gif" \
               "\nWhat is/Who is/Tell me about ...=> For wiki content\nrate ...=> For rating something (out of 10)"
listener = rec.Recognizer()


def speak(dialogue):
    if not os.path.exists('temp'):
        os.makedirs('temp')
    rand_str = random_str()
    tts = gTTS(dialogue, lang='en')
    tts.save("temp/"+rand_str)
    playsound.playsound("temp/"+rand_str)


def commanding():
    try:
        with rec.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=1)
            root.update()
            Label(text="Listening...").pack()
            root.update()
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            root.update()
            Label(text=command).pack()
            root.update()
            Label(text='Processing please be patient..').pack()
            root.update()
            return command
    except Exception as c:
        pass


def run_program():
    command = commanding()
    root.update()
    if 'play' in command:
        root.update()
        song = command.partition('play')
        song = str(song[-1])
        v = 'playing '+song+' on youtube'
        speak(v)
        root.update()
        Label(text='playing ' + song + ' on youtube').pack()
        pywhatkit.playonyt(song)
        root.update()
    elif 'rate' in command:
        a = random.randint(0, 11)
        cmd = command.partition('rate')
        cmd = cmd[-1]
        root.update()
        Label(text=str(a)+'/10').pack()
        root.update()
        b = 'I rate '+cmd+' '+str(a)+' out of 10'
        speak(b)
        root.update()
    elif 'command help' in command:
        root.update()
        Label(text=help_command).pack()
        root.update()
    elif 'time' in command:
        root.update()
        speak("Current time is "+datetime.datetime.now().strftime('%I:%M %p'))
        root.update()
        Label(text="Current time is "+datetime.datetime.now().strftime('%I:%M %p')).pack()
        root.update()
    elif 'joke' in command:
        root.update()
        speak(pyjokes.get_joke('en', 'all'))
        root.update()

    elif 'funny' in command:
        t = tenorpy.Tenor()
        gif_url = t.random("Funny")
        urllib.request.urlretrieve(gif_url, "temp/temp.gif")
        img = PIL.Image.open("temp/temp.gif")
        img.show()

    elif 'what' in command:
        cmd = command.partition('is')
        cmd = str(cmd[-1])
        root.update()
        try:
            info = wikipedia.summary(cmd)
            root.update()
            speak(info)
            root.update()
            Label(text=info).pack()
        except:
            speak("No information available on wikipedia")
            speak("I am searching on google. Please be patient")
            webbrowser.get('windows-default').open('http://www.google.com/?#q='+cmd)

    elif 'who' in command:
        cmd = command.partition('is')
        cmd = str(cmd[-1])
        root.update()
        try:
            info = wikipedia.summary(cmd)
            root.update()
            speak(info)
            root.update()
            Label(text=info).pack()
        except:
            speak("No information available on wikipedia")
            speak("I am searching on google. Please be patient")
            webbrowser.get('windows-default').open('http://www.google.com/?#q='+cmd)

    elif 'tell' in command:
        cmd = command.partition('about')
        cmd = str(cmd[-1])
        try:
            root.update()
            info = wikipedia.summary(cmd)
            root.update()
            speak(info)
            root.update()
            Label(text=info).pack()
        except:
            speak("No information available on wikipedia")
            speak("I am searching on google. Please be patient")
            webbrowser.get('windows-default').open('http://www.google.com/?#q='+cmd)
    else:
        speak("Please wait I am searching for it")
        cmd = command
        webbrowser.get('windows-default').open('http://www.google.com/?#q='+cmd)
    try:
        remove_temp()
    except Exception as e:
        print(e)


# GUI -
root = Tk()
root.geometry("600x600")
root.minsize(500, 500)
root.title("Sid's Assistant")
root.configure(background="grey")
root.iconbitmap("icon.ico")


title = Label(text="Sid's Assistant", background="blue", fg="white", padx=12, pady=5, font=("arial", 19, "bold"))\
    .pack(fill=X)

speak_button = Button(root, text="Click To Speak", fg="white", background="black", pady=5,
                      font=("Arial", 10, "bold"), command=run_program)
speak_button.pack(side=BOTTOM, fill=X)


root.mainloop()
