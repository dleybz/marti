"""Think module which takes in the user's input and responds based on OpenAI's API"""
import openai
import config

openai.organization = config.openai_org
openai.api_key = config.openai_key


def response(user_input: str):
    """take user's input, generate a response"""
    openai_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="You are a beginner Spanish teacher named Marti. You correct your students when they say something incorrectly in Spanish and otherwise respond conversationally. A student says to you"
        + user_input,
        temperature=0.7,
        max_tokens=256,
    )

    print("Marti's Output: " + openai_response.choices[0].text)
    return openai_response.choices[0].text
