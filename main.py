from tkinter import *
import PIL
import speech_recognition as rec
import pywhatkit
import datetime
import wikipedia
import pyjokes
from gtts import gTTS
import tenorpy
import playsound
import urllib
import random
import string
import pyttsx3
import os
import time
# todo in playing voice with gtts do a random string instead of voices.mp3


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
    # engine = pyttsx3.init()
    # engine.setProperty("rate", 110)
    # engine.say(dialogue)
    # engine.runAndWait()
    if not os.path.exists('sample'):
        os.makedirs('sample')
    rand_str = random_str()
    tts = gTTS(dialogue, lang='hi')
    tts.save("sample/"+rand_str)
    playsound.playsound("sample/"+rand_str)


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
        print(c)


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
        urllib.request.urlretrieve(gif_url, "sample/sample.gif")
        img = PIL.Image.open("sample/sample.gif")
        img.show()

    elif 'what' or 'who' or 'tell' in command:
        try:
            if 'is' in command:
                cmd = command.partition('is')
                cmd = str(cmd[-1])
            elif 'tell' in command:
                cmd = command.partition('about')
                cmd = str(cmd[-1])
            root.update()
            info = wikipedia.summary(cmd)
            root.update()
            speak(info)
            root.update()
            Label(text=info).pack()
        except:
            speak('Sorry no information available on ' + command)
            Label(text='Sorry no information available on ' + command).pack()


# GUI -
root = Tk()
root.geometry("600x600")
root.minsize(500, 500)
root.title("Sid's Assistant")
root.configure(background="grey")


title = Label(text="Sid's Assistant", background="blue", fg="white", padx=12, pady=5, font=("arial", 19, "bold"))\
    .pack(fill=X)

speak_button = Button(root, text="Click To Speak", fg="white", background="black", pady=5,
                      font=("Arial", 10, "bold"), command=run_program)
speak_button.pack(side=BOTTOM, fill=X)


root.mainloop()
