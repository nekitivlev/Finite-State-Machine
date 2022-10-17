import ply.yacc as yacc
import sys
import re

from lexer import tokens


class FSM:
    states = set()
    input_alphabet = set()
    initial_state = None
    finite_states = set()
    transition = dict()

    def print(self):
        out = "Finite state machine consist:\n"
        out += "states: " + ', '.join(self.states) + "\n"
        out += "start: " + ', '.join(self.initial_state) + "\n"
        out += "finite states: " + ', '.join(self.finite_states) + "\n"
        out += "alphabet: " + ', '.join(self.input_alphabet) + "\n"
        out += "Rules: \n"
        for x in self.transition:
            out += f"({x[0]})-{x[1]}->({self.transition[x]}), "
        return out

    def clear(self):
        self.states.clear()
        self.input_alphabet.clear()
        self.initial_state = None
        self.finite_states.clear()
        self.transition.clear()


fsm_global = FSM()


def p_error(p):
    if p == None:
        print("end of file")
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"
    print(f"Syntax error: Unexpected {token}")


def p_states(p):
    'start : STATES ASSIGNMENT SET'
    fsm_global.states = set([state.replace('\,',',') for state in re.split(r'(?<!\\),', p[3])])


def p_alphabet(p):
    'start : ALPHABET ASSIGNMENT SET'
    fsm_global.input_alphabet = set([state.replace('\,',',') for state in re.split(r'(?<!\\),', p[3])])


def p_start(p):
    'start : INITIAL ASSIGNMENT SET'
    if len([state.replace('\,',',') for state in re.split(r'(?<!\\),', p[3]) ]) != 1:
        print ("invalid initial state: " + p[3])
    else:
        fsm_global.initial_state = p[3]


def p_finite(p):
    'start : FINITE ASSIGNMENT SET'
    for state in re.split(r'(?<!\\),', p[3]):
        state = state.replace('\,', ',')
        if state in fsm_global.states:
            fsm_global.finite_states.add(state)
        else:
            print("invalid finite state: " + state)


def p_transition(p):
    'start : STATE BINDING SYMBOL TRANSITION STATE'
    if p[1] not in fsm_global.states:
        return print(p[1] + " is not state")
    if p[3] not in fsm_global.input_alphabet:
        return print(p[3] + " is not in alphabet")
    if p[5] not in fsm_global.states:
        return print(p[5] + " is not state")
    fsm_global.transition[(p[1], p[3])] = p[5]


def read_fsm(file, parser):
    fsm_global.clear()
    rfile = open(file)
    wfile = open(sys.argv[1] + ".out", 'w')
    for line in rfile.readlines():
        parser.parse(line)
    wfile.write(fsm_global.print())
    return fsm_global


def main():
    parser = yacc.yacc()
    read_fsm(sys.argv[1], parser)


if __name__ == "__main__":
    main()
