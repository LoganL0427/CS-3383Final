def parse_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    content = content.replace(' ', '').replace('\n', '')
    return content

def extract_tuple(s, startConfig):
    depth = 0
    for i in range(startConfig, len(s)):
        if s[i] == '(':
            depth += 1
        elif s[i] == ')':
            depth -= 1
            if depth == 0:
                return s[startConfig+1:i], i
            
def split_top_level(s):
    depth = 0
    current = ''
    items = []

    for ch in s:
        if ch == '(':
            depth += 1
            current += ch
        elif ch == ')':
            depth -= 1
            current += ch
        elif ch == ',' and depth == 0:
            items.append(current)
            current = ''
        else:
            current += ch
    
    if current.strip():
        items.append(current)
    return items

def get_nfa_data(filename):
    content = parse_file(filename)
    outer_content, _ = extract_tuple(content, 0)
    parts = split_top_level(outer_content)

    alpha_tuple, _ = extract_tuple(parts[0], 0)
    nfa_components = split_top_level(alpha_tuple)

    alphabet, _ = extract_tuple(nfa_components[0], 0)
    split_alphabet = split_top_level(alphabet)

    states, _ = extract_tuple(nfa_components[1], 0)
    split_states = split_top_level(states)

    start_state = nfa_components[2]

    final_state, _ = extract_tuple(nfa_components[3], 0)
    split_final_state = split_top_level(final_state)

    transitions, _ = extract_tuple(nfa_components[4], 0)
    split_transitions = split_top_level(transitions)

    transition_dictionary = {}

    for t in split_transitions:
        inner_t, _ = extract_tuple(t, 0)
        parts_t = split_top_level(inner_t)

        from_state = parts_t[0]
        symbol = parts_t[1]
        to_state = parts_t[2]

        key = (from_state, symbol)

        if key not in transition_dictionary:
            transition_dictionary[key] = []
        
        transition_dictionary[key].append(to_state)

    return {
        'alphabet': set(split_alphabet),
        'states': set(split_states),
        'start': start_state,
        'accepting': set(split_final_state),
        'transitions': transition_dictionary
    }