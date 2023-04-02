# Speech-to-Text Benchmark

This repo contains the code, results, and analysis for my [comprehensive speech-to-text benchmark](https://martiai.substack.com/p/stt-benchmark).

The main file is testing.py, which iterates through all of the samples in `/samples/easy/`, which were generated with `record_samples.py`. `testing.py` passes the samples to the `test_options()` function in `test_hear.py`, which runs each sample through each of the following speech-to-text options:
* Google Translate
* Picovoice Leopard
* Amazon Web Services
* Microsoft Azure
* AssemblyAI
* Local Whisper
* Hosted Whisper
* CMU Sphinx
* Deepgram
* Wit.ai
* Houndify
* Voicegain
* Google Cloud Platform
* Alpha Cephei Vosk

In addition to collecting the transcription from the service, `test_options()` also collects the time that it takes to generate the transcription ("latency") and a number of different accuracy measurements.

These results are saved in `raw_results.csv` and then analyzed in `analysis.ipynb`.

## Requirements

In addition to the packages required to access the various SDKs and APIs for the STT options, this benchmark also requires a `config.py` file populated with access credentials that looks like:
```python
WIT_SAT = ""

AZURE_KEY = ""

HOUNDIFY_ID = ""
HOUNDIFY_KEY = ""

IBM_KEY = ""
IBM_USER = ""

OPENAI_ORG = ""
OPENAI_KEY = ""

ASSEMBLY_KEY = ""

AWS_ACCESS = ""
AWS_SECRET = ""
AWS_BUCKET = ""

DEEPGRAM_SECRET = ""

PICOVOICE_KEY = "=="

VOICEGAIN_JWT = ""
VOICEGAIN_KEY = ""
```
and a `gcp_cred.json` file that can be generated in GCP.

## Contact
If you have any questions about the benchmark methodology or results, are having trouble running the benchmark, or have some transcribed speech you want me to benchmark for you, contact me at: `danny [dot] leybzon [at] gmail [dot] com`