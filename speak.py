# from https://stackoverflow.com/questions/58614450/is-there-a-module-that-allows-me-to-make-python-say-things-as-audio-through-the
# need to install ffmpeg

from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

def output(response):
    tts = gTTS(text=response, lang='es')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    song = AudioSegment.from_file(fp, format="mp3")
    play(song)
    return None

def end_convo():
    tts = gTTS(text="thank you, goodbye", lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    song = AudioSegment.from_file(fp, format="mp3")
    print("Ending the conversation. Thank you, goodbye")
    play(song)
    return None