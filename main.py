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
import os


help_command = "Play ... => to play some media\nTell me the time => For current time\n" \
               "tell me a joke => For joke(mainly programming)\nShow me something funny => For funny gif" \
               "\nWhat is/Who is/Tell me about ...=> For wiki content\nrate ...=> For rating something (out of 10)"
listener = rec.Recognizer()


def speak(dialogue):
    tts = gTTS(dialogue, lang_check=True)
    tts.save('voice.mp3')
    playsound.playsound('voice.mp3')


def commanding():
    try:
        with rec.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(command)
            print('Processing please be patient..')
            return command
    except Exception as c:
        print(c)


def run_program():
    command = commanding()
    if 'play' in command:
        song = command.partition('play')
        song = str(song[-1])
        speak('playing '+song+' on youtube')
        pywhatkit.playonyt(song)
    elif 'rate' in command:
        a = random.randint(0, 11)
        cmd = command.partition('rate')
        cmd = cmd[-1]
        print(str(a)+'/10')
        speak('I rate '+cmd+' '+str(a)+' out of 10')
    elif 'command help' in command:
        print(help_command)
    elif 'time' in command:
        speak("Current time is "+datetime.datetime.now().strftime('%I:%M %p'))
    elif 'joke' in command:
        speak(pyjokes.get_joke('en', 'all'))

    elif 'funny' in command:
        t = tenorpy.Tenor()
        gif_url = t.random("Funny")
        urllib.request.urlretrieve(gif_url, "sample.gif")
        img = PIL.Image.open("sample.gif")
        img.show()

    elif 'what' or 'who' or 'tell' in command:
        try:
            if 'is' in command:
                cmd = command.partition('is')
                cmd = str(cmd[-1])
            elif 'tell' in command:
                cmd = command.partition('about')
                cmd = str(cmd[-1])
            info = wikipedia.summary(cmd)
            speak(info)
            print(info)
        except:
            speak('Sorry no information available on ' + command)


run_program()
