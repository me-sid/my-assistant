from tkinter import *
from tkinter import ttk
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
root = Tk()
root.geometry("600x600")
root.minsize(500, 500)
root.title("Sid's Assistant")
root.iconbitmap("icon.ico")
root.configure(background="dark grey")

# Frames
f1 = Frame(root, background="dark grey")
f1.pack(side=TOP, fill=X)

f2 = Frame(root, background="dark grey", padx=7)
f2.pack(fill=BOTH)

f3 = Frame(root, background="black")
f3.pack(side=BOTTOM, fill=X)

title_label = Label(f1, text="SciPi", fg="aqua", background="dark grey", font=("Roboto", 20, "bold"))
title_label.pack()


# Message Functions
def user_msg(text):
    Label(f2, text=text, background="light blue", fg="black", justify=RIGHT).pack(anchor="ne")


def assistant_msg(text):
    Label(f2, text=text, background="light blue", fg="black", justify=LEFT).pack(anchor='nw')


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
            assistant_msg('Listening')
            root.update()
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            root.update()
            command = command.lower()
            root.update()
            user_msg(command)
            root.update()
            assistant_msg('Processing please be patient..')
            root.update()
            return command
    except Exception as c:
        print(c)


def run_program():
    command = commanding()
    root.update()
    if 'play' in command:
        root.update()
        cmd = command.partition('play')
        cmd = str(cmd[-1])
        root.update()
        v = 'playing '+cmd+' on youtube'
        speak(v)
        root.update()
        assistant_msg('playing ' + cmd + ' on youtube')
        root.update()
        pywhatkit.playonyt(cmd)
        root.update()
    elif 'rate' in command:
        a = random.randint(0, 11)
        root.update()
        cmd = command.partition('rate')
        root.update()
        cmd = cmd[-1]
        root.update()
        assistant_msg(str(a)+'/10')
        root.update()
        b = 'I rate '+cmd+' '+str(a)+' out of 10'
        root.update()
        speak(b)
        root.update()
    elif 'command help' in command:
        root.update()
        assistant_msg(help_command)
        root.update()
    elif 'time' in command:
        root.update()
        speak("Current time is "+datetime.datetime.now().strftime('%I:%M %p'))
        root.update()
        assistant_msg("Current time is "+datetime.datetime.now().strftime('%I:%M %p'))
        root.update()
    elif 'joke' in command:
        root.update()
        joke = pyjokes.get_joke('en', 'all')
        speak(joke)
        root.update()
        assistant_msg(joke)
        root.update()
    elif 'funny' in command:
        speak('Please wait, I am showing you something funny')
        root.update()
        t = tenorpy.Tenor()
        gif_url = t.random("Funny")
        root.update()
        urllib.request.urlretrieve(gif_url, "temp/temp.gif")
        root.update()
        img = PIL.Image.open("temp/temp.gif")
        root.update()
        img.show()
        root.update()

    elif 'what' in command:
        cmd = command.partition('is')
        cmd = str(cmd[-1])
        root.update()
        try:
            info = wikipedia.summary(cmd, sentences=3)
            info = info.replace(".", ".\n")
            root.update()
            speak(info)
            root.update()
            assistant_msg(info)
            root.update()
        except:
            root.update()
            speak("I am searching for it. Please be patient")
            root.update()
            assistant_msg("I am searching for it. Please be patient")
            root.update()
            webbrowser.get('windows-default').open('http://www.google.com/?#q='+cmd)

    elif 'who' in command:
        cmd = command.partition('is')
        cmd = str(cmd[-1])
        root.update()
        try:
            info = wikipedia.summary(cmd, sentences=3)
            info = info.replace(".", ".\n")
            root.update()
            assistant_msg(text=info)
            root.update()
            speak(info)
            root.update()
        except:
            root.update()
            speak("I am searching for it. Please be patient")
            root.update()
            assistant_msg("I am searching for it. Please be patient")
            root.update()
            webbrowser.get('windows-default').open('http://www.google.com/?#q='+cmd)
            root.update()

    elif 'tell' in command:
        cmd = command.partition('about')
        root.update()
        cmd = str(cmd[-1])
        root.update()
        try:
            root.update()
            info = wikipedia.summary(cmd, sentences=3)
            info = info.replace(".", ".\n")
            root.update()
            speak(info)
            root.update()
            assistant_msg(text=info)
            root.update()
        except:
            root.update()
            speak("I am searching for it. Please be patient")
            root.update()
            assistant_msg("I am searching for it. Please be patient")
            root.update()
            webbrowser.get('windows-default').open('http://www.google.com/?#q='+cmd)
            root.update()
    else:
        root.update()
        speak("Please wait I am searching for it")
        root.update()
        assistant_msg("Please wait I am searching for it")
        cmd = command
        root.update()
        webbrowser.get('windows-default').open('http://www.google.com/?#q='+cmd)
    try:
        remove_temp()
    except Exception as e:
        print(e)


def greet():
    speak('Hi, How can I help you')
    assistant_msg('Hi\nHow can I help you?')


greet()

speak_btn = Button(f3, text="Click to speak", command=run_program)
speak_btn.pack(fill=X)

root.mainloop()
