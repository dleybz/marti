"""Program for recording test samples for the benchmark"""

# referencing https://github.com/Uberi/speech_recognition/blob/master/examples/write_audio.py
import os
import speech_recognition as sr # pylint: disable=import-error

# obtain audio from the microphone
r = sr.Recognizer()
while True:
    with sr.Microphone() as source:
        # create a sample folder if it doesn't already exist
        if not os.path.exists("samples"):
            os.makedirs("samples")

        # gather user input
        sample_name = input("Enter a name for this sample: ")
        sample_difficulty = input("Enter a difficulty for this sample: ")

        # create a difficulty folder if it doesn't already exist
        if not os.path.exists("samples/" + sample_difficulty):
            os.makedirs("samples/" + sample_difficulty)

        # record user sample
        write_location = "samples/" + sample_difficulty + "/" + sample_name + ".wav"
        print("Speak a sample and it will be saved at " + write_location)
        audio = r.listen(source)

    # write audio to a WAV file
    with open(write_location, "wb") as f:
        f.write(audio.get_wav_data())
