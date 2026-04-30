import re
import ast

arr_valid_states = [] 

'''
By: Caden Brannan, Logan Little, Manuel Cruz, and Brett Raheem 
'''


## As implied, this stores all individual transitions into dot addressable variables.
## The NFA itself is formalised into a similar object 
class Transition:
    def __init__(self, start_state, symbol, end_state):
        self.start_state = start_state
        self.symbol = symbol
        self.end_state = end_state

    def __repr__(self):
        return f"({self.start_state}, {self.symbol}, {self.end_state})"


class NFA:
    def __init__(self, alphabet, states, start_state, final_states, deltas):
        self.alphabet = alphabet
        self.states = states
        self.start_state = start_state
        self.final_states = final_states
        self.deltas = deltas



## the parser for the text file is provided by chatgpt, including comments 
## the parser includes the __quote_symbols, _quote_digits, _prepare, and process_NFA methods. 
def _quote_symbols(text):
    # quote bare words like q0, q1 but not numbers
    return re.sub(r'\b(q\d+)\b', r'"\1"', text)


def _quote_digits(text):
    # turn (0, 1) into ("0","1") so alphabet is strings
    return re.sub(r'(?<=\(|,)\s*(\d+)\s*(?=,|\))', r'"\1"', text)


def _prepare(text):
    text = text.strip()
    text = _quote_symbols(text)
    text = _quote_digits(text)
    return text


def process_NFA(file_path):
    with open(file_path, "r") as f:
        raw = f.read()

    cleaned = _prepare(raw)

    data = ast.literal_eval(cleaned)

    nfa_tuple, test_strings = data

    alphabet, states, start_state, final_states, transitions = nfa_tuple

    deltas = []
    for (s, sym, e) in transitions:
        deltas.append(Transition(s, sym, e))

    nfa = NFA(
        alphabet=list(alphabet),
        states=list(states),
        start_state=start_state,
        final_states=(final_states),
        deltas=deltas
    )

    return nfa, list(test_strings)



## The method here differs from the algorithm idea presented in the course by using a recursive, depth based approach. 
## Tather than manual stack management, the call stack is used instead. It is implicit popping and pushing. 
## The advantage it is very basic to write. the disadvantage is that it increases time and space complexity massively-
## - however this is irrelevant given our small toy examples -
## - and the fact that it will stop as soon as a single valid configuration is found.

def is_string_accepted(state, string, index, NFA):
    ##if we've reached the end of the string, and its not in a final state, it went into a dead end. 
    if index >= len(string):
        return state in NFA.final_states

    ## establish which symbol from the string is being processed: 
    symbol = string[index]

    ## filter out symbols the machine does not accept
    if symbol not in NFA.alphabet:
        return False

    ##compute all paths this state leads to with this symbol. 
    valid_states = []
    for delta in NFA.deltas:
        if delta.start_state == state and delta.symbol == symbol:
            valid_states.append(delta.end_state)


    ## explore all possible sub paths from here forward.
    ## this avoids the need for randomness but fulfils the NFA capability
    ## somewhat like depth traversal in a graph. 
    for next_state in valid_states:
       if is_string_accepted(next_state, string, index + 1, NFA):
        return True

    return False


## quite literally mimics the behaviour demonstrated the assignment PDF. 
def main(): 
    file_name = input("Please input the file name: ").strip()

    ## filter out bad files.
    try:
        nfa, test_strings = process_NFA(file_name)
    except Exception as e:
        print("Error reading file:", e)
        raise

    first = True

    ## if pre-made strings are given, read only those. 
    ## this is made to literally print parenthesis as well, for sake of 100% following the project PDF.
    if len(test_strings) != 0: 
        results = ""
        results = results + ("(")
        for string in test_strings:
            if is_string_accepted(nfa.start_state, string, 0, nfa) == True: 
                results = results + ("accepted")
            else:
                results = results + ("rejected")
            results = results + (", ") 
        results = results + (")")
        results  = results.replace(", )",")")
        print(results)
        return 



    ## setup infinite loop 
    while True:
        if first:
            user_input = input("Please input a string: ").strip()
            first = False
        else:
            user_input = input("Please input another string: ").strip()

        if user_input == "":
            print("Bye bye.")
            break

        accepted = is_string_accepted(nfa.start_state, user_input, 0, nfa)

        if accepted:
            print("Accepted.")
        else:
            print("Rejected.")

## entry point for VS code testing. 
if __name__ == "__main__":
    main()
