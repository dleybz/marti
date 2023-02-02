import openai
import config

openai.organization = config.openai_org
openai.api_key = config.openai_key

def response(input):
  response = openai.Completion.create(
    engine="text-davinci-003",
    prompt="You are a beginner Spanish teacher named Marti. You correct your students when they say something incorrectly in Spanish and otherwise respond conversationally. A student says to you" + input,
    temperature = 0.7,
    max_tokens = 256
  )

  print("Marti's Output: " + response.choices[0].text)
  return response.choices[0].text