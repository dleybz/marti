import hear
import think
import speak


def main():
    while(True):
        input = hear.input()
        if "finish conversation" not in input:
            response = think.response(input)
            speak.output(response)
        else:
            speak.end_convo()
            break

if __name__ == "__main__":
    main()