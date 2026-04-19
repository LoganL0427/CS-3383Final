
nfa = {
    'alphabet': {'0','1'},
    'states': {'q0', 'q1', 'q2'},
    'start': 'q0',
    'accepting': {'q2'},
    'transition': {
        ('q0', '0'): ['q0', 'q1'],
        ('q0', '1'): ['q0'],
        ('q1', '1'): ['q2']
    }
}