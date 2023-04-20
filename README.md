# Marti: an AI-powered language tutor
Imagine having a language tutor with whom you can converse from your phone or laptop at any time. A tutor who is a master of the language that you want to learn and personalizes their instruction to your ability. This is the goal of Marti.

Marti (a syllabalic abbreviation of “maestro artificial”—“synthetic teacher” in Spanish) spawned from a series of discussions that I had over the course of January 2023. I am [extremely bullish](https://martiai.substack.com/p/why-this-project) on the power of AI to make personal tutoring more accessible (more on this in a later post) and wanted to dip my toe into the water by getting my hands dirty with a project.

## Video Demo
[![Watch the video](https://img.youtube.com/vi/KiSo1hbSSPg/maxresdefault.jpg)](https://www.youtube.com/watch?v=KiSo1hbSSPg)

## Running Marti
To run Marti on your own machine, simply clone this repo, install the packages specified in `requirements.txt`, and run the `marti.py` file. You'll be prompted to start speaking with Marti. In addition to the files in this repo, you'll also need to generate a `config.py` file with [OpenAI API Keys](https://platform.openai.com/docs/api-reference/authentication) with the following format:
```python
openai_org = "org-yourorgid"
openai_key = "youropenaikey"
```

## Other branches
Other branches in this repository are used to store the code that was used for tests related to this project. These include a latency analysis of different modules in Marti as well as a benchmark of different speech-to-text options.

## Learn more
To learn more about Marti, you can read the [Substack](https://martiai.substack.com/) or email me at `danny [dot] leybzon [at] gmail [dot] com`.
