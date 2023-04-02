"""Program for testing different ASR/STT/transcription/speech recognition APIs"""
# pylint: disable=line-too-long

import time
import os
import sys
import json
import wave
import base64
import requests
from unidecode import unidecode
import openai
from vosk import Model, KaldiRecognizer, SetLogLevel
import speech_recognition as sr
import jiwer
import boto3
from deepgram import Deepgram
import pvleopard
import voicegain_speech

import config

class HiddenPrints:
    """Used to hide ugly output"""
    def __enter__(self):
        self._original_stdout = sys.stdout # pylint: disable=attribute-defined-outside-init
        sys.stdout = open(os.devnull, 'w') # pylint: disable=unspecified-encoding

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def test_similarity(ground_truth: str, hypothesis: str):
    """Returns wer, mer, and wil, given two pieces of text"""
    measures = jiwer.compute_measures(ground_truth, hypothesis)
    wer = measures['wer']
    mer = measures['mer']
    wil = measures['wil']

    return wer, mer, wil

def test_options(input_audio_path: str, input_text: str):
    """Tests audio against each speech recognition API"""

    # test SR APIs
    recognizer = sr.Recognizer()
    with sr.AudioFile(input_audio_path) as source:
        sr_audio = recognizer.record(source)  # read the entire audio file
    speech_recognition_apis = ["sphinx", "google", "whisper", "wit", "google_cloud", "azure", "houndify"]
    # newest IBM API wasn't supported at the time of writing
    # Tensorflow v2 breaks SpeechRecognition
    results = [test_sr_api(sr_api, recognizer, sr_audio, input_text) for sr_api in speech_recognition_apis]

    #add the Voicegain results to the list of results
    voicegain_results = test_voicegain(input_audio_path, input_text)
    results.append(voicegain_results)

    #add the Picovoice results to the list of results
    picovoice_results = test_picovoice(input_audio_path, input_text)
    results.append(picovoice_results)

    #add the Whisper API results to the list of results
    whisper_api_results = test_openai_whisper(input_audio_path, input_text)
    results.append(whisper_api_results)

    #add the Vosk results to the list of results
    vosk_results = test_vosk(input_audio_path, input_text)
    results.append(vosk_results)

    #add the Assembly AI results to the list of results
    assemblyai_results = test_assemblyai(input_audio_path, input_text)
    results.append(assemblyai_results)

    #add the AWS Transcribe results to the list of results
    aws_results = test_aws(input_audio_path, input_text)
    results.append(aws_results)

    #add the Deepgram to the list of results
    deepgram_results = test_deepgram(input_audio_path, input_text)
    results.append(deepgram_results)

    print("Results for this sample: " + str(results))

    return results

def collect_api_metrics(api_name: str, function_string: str, input_text: str, recognizer: sr.Recognizer = None, sr_audio: sr.AudioFile = None, audio_file = None, wf_data = None, rec = None, upload_endpoint: str = None, transcript_endpoint: str = None, header: dict = None, file_name: str = None, dg_client = None, dg_source = None, pv_client = None, vg_api: voicegain_speech.TranscribeApi = None): # pylint: disable=unused-argument, line-too-long
    """Collects metrics for a specific API"""
    start_time = time.time()
    with HiddenPrints():
        api_output = eval(function_string) # pylint: disable=eval-used
    time_taken = time.time() - start_time

    if api_name in ["azure", "houndify"]:
        api_output = api_output[0]

    if api_name == "vosk":
        inter_output = rec.Result()
        api_output = json.loads(inter_output)["text"]

    to_print = "API: " + api_name + ", Time: " + str(time_taken) + ", Output: " + api_output
    print(to_print)

    # strip punctuation from input and output
    punct_to_remove = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~¿"
    depunctuated_predicted = unidecode(api_output.translate(str.maketrans('', '', punct_to_remove))).lower()
    depunctuated_correct = unidecode(input_text.translate(str.maketrans('', '', punct_to_remove))).lower()

    # test accuracy metrics of the API
    wer, mer, wil = test_similarity(depunctuated_correct, depunctuated_predicted)

    results = [input_text, api_name, time_taken, wer, mer, wil]

    return results

def test_sr_api(api_name: str, recognizer: sr.Recognizer, sr_audio: sr.AudioFile, correct_text: str):
    """Tests audio against a specific SpeechRecognition API"""

    # define a dictionary of each API's arguments
    recognize_arguments = {
        "sphinx": "", # not customized to Spanish
        "google": ", language = 'es-ES'",
        "whisper": ", model = 'tiny', language = 'spanish'",
        "wit": ", key  = '" + config.WIT_SAT + "'",
        "google_cloud": ", credentials_json = 'gcp_cred.json', language = 'es-ES'",
        "azure": ", key = '" + config.AZURE_KEY + "', language = 'es-ES'",
        "houndify": ", client_id = '" + config.HOUNDIFY_ID + "', client_key = '" + config.HOUNDIFY_KEY + "'", 
        "vosk": ", language = 'es-ES'"
    }

    # can't use literal_eval because we're using non-literal data types
    str_to_eval = "recognizer.recognize_" + api_name + "(sr_audio" + recognize_arguments[api_name] + ")"

    return collect_api_metrics(api_name, str_to_eval, correct_text, recognizer = recognizer, sr_audio = sr_audio)

def test_openai_whisper(audio_path: str, correct_text: str):
    """Access OpenAI's Whisper API"""
    openai.organization = config.OPENAI_ORG
    openai.api_key = config.OPENAI_KEY

    audio_file = open(audio_path, "rb")

    str_to_eval = 'openai.Audio.transcribe("whisper-1", audio_file, language = "es")["text"]'

    return collect_api_metrics("openai_whisper", str_to_eval, correct_text, audio_file = audio_file)

def test_vosk(audio_path: str, correct_text: str):
    """Access Vosk's API"""
    SetLogLevel(-1)

    wave_form = wave.open(audio_path, "rb")
    es_model = Model("model")
    rec = KaldiRecognizer(es_model, wave_form.getframerate())
    rec.SetWords(True)
    rec.SetPartialWords(True)
    num_frames = wave_form.getnframes()
    data = wave_form.readframes(num_frames)

    string_to_eval = "rec.AcceptWaveform(wf_data)"

    return collect_api_metrics("vosk", string_to_eval , correct_text, wf_data = data, rec = rec)

def test_assemblyai(audio_path: str, correct_text: str):
    """Access Assembly AI's API"""    
    upload_endpoint = "https://api.assemblyai.com/v2/upload"
    transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
    header = {
	    'authorization': config.ASSEMBLY_KEY,
	    'content-type': 'application/json'
    }
    audio = open(audio_path, "rb").read(5242880)

    string_to_eval = "post_to_assemblyai(audio_file, upload_endpoint, transcript_endpoint, header)"

    return collect_api_metrics("assemblyai", string_to_eval , correct_text, audio_file = audio, upload_endpoint = upload_endpoint, transcript_endpoint = transcript_endpoint, header = header)

def post_to_assemblyai(audio, upload_endpoint: str, transcript_endpoint: str, header: dict):
    """Helper function for test_assemblyai"""
    upload_response = requests.post(
        upload_endpoint,
        headers=header,
        data=audio,
        timeout=999999
    ).json()

    transcript_request = {
        'audio_url': upload_response['upload_url'],
        "language_code": "es"
    }

    transcript_response = requests.post(
        transcript_endpoint,
        json=transcript_request,
        headers=header,
        timeout=999999
    ).json()

    polling_endpoint = "https://api.assemblyai.com/v2/transcript/"
    polling_endpoint += transcript_response['id']

    while True:
        polling_response = requests.get(polling_endpoint, headers=header, timeout=999999)
        polling_response = polling_response.json()

        if polling_response['status'] == 'completed':
            break

        time.sleep(5)

    return polling_response['text']

def test_aws(file_name: str, correct_text: str):
    """Access AWS's API"""
    string_to_eval = "aws_mono(file_name)"

    return collect_api_metrics("aws", string_to_eval, correct_text, file_name=file_name)

def aws_mono(file_name: str):
    """Ugly single function to upload, transcribe, and parse AWS output"""

    #upload
    s3_client = boto3.client('s3', aws_access_key_id = config.AWS_ACCESS, aws_secret_access_key = config.AWS_SECRET, region_name = "us-east-1")

    s3_client.create_bucket(Bucket=config.AWS_BUCKET)

    s3_client.upload_file(file_name, config.AWS_BUCKET, file_name)

    #start job
    file_uri = "s3://" + config.AWS_BUCKET + "/" + file_name
    job_name = file_name.split("/")[-1]
    output_key = file_name + ".json"

    transcribe_client = boto3.client('transcribe', aws_access_key_id = config.AWS_ACCESS, aws_secret_access_key = config.AWS_SECRET, region_name = "us-east-1")

    # start transcription job. If error, delete job and try again
    try:
        transcribe_client.start_transcription_job(TranscriptionJobName = job_name, LanguageCode = "es-US", Media = {"MediaFileUri": file_uri}, MediaFormat = "wav", OutputBucketName = config.AWS_BUCKET, OutputKey = output_key)
    except: # pylint: disable=bare-except
        transcribe_client.delete_transcription_job(TranscriptionJobName = job_name)
        transcribe_client.start_transcription_job(TranscriptionJobName = job_name, LanguageCode = "es-US", Media = {"MediaFileUri": file_uri}, MediaFormat = "wav", OutputBucketName = config.AWS_BUCKET, OutputKey = output_key)

    while True:
        result = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        if result['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        time.sleep(1)

    # get output
    output = s3_client.get_object(Bucket = config.AWS_BUCKET, Key = output_key)

    output = output["Body"].read().decode("utf-8")

    output = json.loads(output)

    return output["results"]["transcripts"][0]["transcript"]

def test_deepgram(file_name: str, correct_text: str):
    """Access Deepgram's API"""
    dg_client = Deepgram(config.DEEPGRAM_SECRET)

    audio_file = open(file_name, "rb")
    dg_source = {'buffer': audio_file, 'mimetype': "wav"}

    string_to_eval = "dg_client.transcription.sync_prerecorded(dg_source, {'language': 'es'})['results']['channels'][0]['alternatives'][0]['transcript']"

    return collect_api_metrics("deepgram", string_to_eval, correct_text, dg_client=dg_client, dg_source=dg_source)

def test_picovoice(file_name: str, correct_text: str):
    """Access Picovoice's API"""
    pv_client = pvleopard.create(access_key = config.PICOVOICE_KEY)

    string_to_eval = "pv_client.process_file(file_name)[0]"

    return collect_api_metrics("picovoice", string_to_eval, correct_text, pv_client=pv_client, file_name=file_name)

def test_voicegain(file_name: str, correct_text: str):
    """Access Voicegain's API"""
    vg_config = voicegain_speech.Configuration()
    vg_config.access_token = config.VOICEGAIN_JWT

    vg_client = voicegain_speech.ApiClient(configuration=vg_config)
    vg_api = voicegain_speech.TranscribeApi(vg_client)

    string_to_eval = "voicegain_helper(file_name, vg_api)"

    return collect_api_metrics("voicegain", string_to_eval, correct_text, file_name=file_name, vg_api=vg_api)

def voicegain_helper(file_name: str, vg_api: voicegain_speech.TranscribeApi):
    """Helper function to access Voicegain's API"""
    with open(file_name, "rb") as file:
        audio_base64 = base64.b64encode(file.read()).decode()

    result = vg_api.asr_transcribe_post(
        sync_transcription_request={
            "audio": {
                "source": {
                    "inline": {
                        "data": audio_base64
                    }
                }
            }
        }
    ).result.alternatives[0].utterance

    return result
