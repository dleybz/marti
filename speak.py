"""Speak module which takes the LLM's response and verbalizes it to the user"""

# from https://stackoverflow.com/questions/58614450/is-there-a-module-that-allows-me-to-make-python-say-things-as-audio-through-the
# need to install ffmpeg

from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play


def output(response: str):
    """take LLM's response, convert to audio and play back"""
    tts = gTTS(text=response, lang="es")
    audio_response = BytesIO()
    tts.write_to_fp(audio_response)
    audio_response.seek(0)

    audio_output = AudioSegment.from_file(audio_response, format="mp3")
    play(audio_output)
    return None


def end_convo():
    """End conversation by saying 'Thank you, goodbye'"""
    tts = gTTS(text="thank you, goodbye", lang="en")
    end_audio = BytesIO()
    tts.write_to_fp(end_audio)
    end_audio.seek(0)

    end_audio = AudioSegment.from_file(end_audio, format="mp3")
    print("Ending the conversation. Thank you, goodbye")
    play(end_audio)
    return None
