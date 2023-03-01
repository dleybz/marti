"""Main file which acts as entrypoint into the program"""
import hear
import think
import speak


def main():
    """main function which acts as an entrypoint into the program. Tests if the user has said "finish conversation", exits if they have, otherwise responds to what they said"""
    while True:
        user_input = hear.user_input()
        if "finish conversation" not in user_input:
            response = think.response(user_input)
            speak.output(response)
        else:
            speak.end_convo()
            break


if __name__ == "__main__":
    main()
