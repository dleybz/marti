import hear
import think
import speak

while(True):
    input = hear.input()
    if "finish conversation" not in input:
        response = think.response(input)
        speak.output(response)
    else:
        speak.end_convo()
        break