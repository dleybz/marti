import openai
import config

import time

openai.organization = config.openai_org
openai.api_key = config.openai_key

def response(input):
  start_time = time.time()
  response = openai.Completion.create(
    engine="text-davinci-003",
    prompt="You are a beginner Spanish teacher named Marti. You correct your students when they say something incorrectly in Spanish and otherwise respond conversationally. A student says to you" + input,
    temperature = 0.7,
    max_tokens = 256
  )
  think_time = time.time()  - start_time
  print("Marti's Output: " + response.choices[0].text)
  print("Think time: " + str(think_time))
  return response.choices[0].text, think_time