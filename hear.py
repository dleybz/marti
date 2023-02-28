#https://realpython.com/python-speech-recognition/#working-with-microphones

import speech_recognition as sr

import time

def input():
    start_time = time.time()
    r = sr.Recognizer()
    mic = sr.Microphone()

    print("System Prompt: What do you want to say to Marti?")
    mic = sr.Microphone()
    with mic as source:
        audio = r.listen(source)
    listen_time = time.time() - start_time
    print("Listen time: " + str(listen_time))

    start_time = time.time()
    text_output = r.recognize_google(audio, show_all=False, with_confidence=False)
    recognize_time = time.time() - start_time
    print("User's Input: " + text_output)
    print("Recognize time: " + str(recognize_time))
    return text_output, listen_time, recognize_time