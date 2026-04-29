# Handles all user-facing input and output for the NFA simulator

from main import is_string_accepted


def run_batch_mode(nfa, test_strings):
    """
    If the file provided non-empty test strings, run all of them
    and print a single results tuple then exit.

    """
    results = []
    for string in test_strings:
        if is_string_accepted(nfa.start_state, string, 0, nfa):
            results.append("accepted")
        else:
            results.append("rejected")

    print("(" + ", ".join(results) + ")")


def run_interactive_mode(nfa):
    """
    If no test strings were provided in the file, prompt the user
    repeatedly until they enter an empty string.

    """
    first = True

    while True:
        if first:
            user_input = input("Please input a string: ").strip()
            first = False
        else:
            user_input = input("Please input another string: ").strip()

        if user_input == "":
            print("Bye bye.")
            break

        if is_string_accepted(nfa.start_state, user_input, 0, nfa):
            print("Accepted.")
        else:
            print("Rejected.")


def get_file_name():
    return input("Please input the file name: ").strip()


def display_file_error(error):
    print("Error reading file:", error)
