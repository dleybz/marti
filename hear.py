"""Hear module which listens for the user's input and transcribes it"""
# referenced: https://realpython.com/python-speech-recognition/#working-with-microphones

import speech_recognition as sr


def user_input():
    """take user's audio, convert it to text"""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("System Prompt: What do you want to say to Marti?")
    mic = sr.Microphone()
    with mic as source:
        audio = recognizer.listen(source)

    text_output = recognizer.recognize_google(audio, show_all=False, with_confidence=False)
    print("User's Input: " + text_output)
    return text_output
