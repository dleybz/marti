#https://realpython.com/python-speech-recognition/#working-with-microphones

import speech_recognition as sr

def input():
    r = sr.Recognizer()
    mic = sr.Microphone()

    print("System Prompt: What do you want to say to Marti?")
    mic = sr.Microphone()
    with mic as source:
        audio = r.listen(source)

    text_output = r.recognize_google(audio, show_all=False, with_confidence=False)
    print("User's Input: " + text_output)
    return text_output