import sys
import re


class TM:
    """
    Class to represent TM
    """

    def __init__(self, states, initial_state, initial_memory_symbol, final_states, transition_functions):
        self.string = ''
        self.states = states
        self.initial_state = initial_state
        self.initial_memory_symbol = initial_memory_symbol
        self.final_states = final_states
        self.transition_functions = transition_functions

        assert self.initial_state in states, "Initial state not in states"
        assert set(self.final_states).issubset(self.states), "Final states is not subset of states"

        self.initialize()

    def initialize(self):
        """
        Setup all values
        """

        self.memory = ['_'] * 1000
        self.memory[0] = self.initial_memory_symbol

        self.pointer_memory = 0
        self.pointer_input = 0

        self.current_state = self.initial_state

    def accept_string(self, string, pprint=False):
        """
        analize the string
        :param string: strign that consist of alphabet
        :return: boolean
        """

        self.string = string + '_'
        self.initialize()
        if pprint:
            print(tm)
        while tm.current_state not in tm.final_states:
            symbol_read = self.string[self.pointer_input]

            found_function = False
            for transition_function in self.transition_functions:
                if transition_function.try_to_apply(self, symbol_read, self.memory[self.pointer_memory]):
                    found_function = True
                    break
            if pprint:
                print(tm)
            if not found_function:
                break

        return tm.current_state in tm.final_states

    def __str__(self):
        """
        :return: string representation of TM
        """
        string = ''.join(list(filter(lambda x: x != '_', self.string)))
        memory = ''.join(list(filter(lambda x: x != '_', self.memory)))
        return str(self.current_state) + ', ' + \
               string[:self.pointer_input] + '^' + string[self.pointer_input:] + \
               ', ' + memory[:self.pointer_memory] + '^' + memory[self.pointer_memory:]


class Transition:
    """
    Class to represent transition between to states
    """

    def __init__(self, from_state, to_state, symbol_read, symbol_on_memory,
                 symbol_put, direction_read, direction_memory):
        self.from_state = from_state
        self.to_state = to_state
        self.symbol_read = symbol_read
        self.symbol_on_memory = symbol_on_memory
        self.symbol_put = symbol_put
        self.direction_read = direction_read
        self.direction_memory = direction_memory

    def try_to_apply(self, tm: TM, symbol_read, symbol_on_memory):
        """
        :param tm: TM instance
        :param symbol_read: string of reading head
        :param symbol_on_memory: string of memory head
        :return: boolean if success
        """
        if self.symbol_read == symbol_read and self.symbol_on_memory == symbol_on_memory and tm.current_state == self.from_state:
            tm.current_state = self.to_state
            tm.memory[tm.pointer_memory] = self.symbol_put
            tm.pointer_input += self.direction_read
            tm.pointer_memory += self.direction_memory
            return True
        else:
            return False


if __name__ == '__main__':
    tr_functions = [Transition('q0', 'q0', '0', 'Z', 'Z', 0, 1),
                    Transition('q0', 'q0', '1', 'Z', 'Z', 0, 1),
                    Transition('q0', 'q0', '0', '_', '0', 1, 1),
                    Transition('q0', 'q0', '1', '_', '1', 1, 1),

                    Transition('q0', 'q1', '#', '_', '_', 1, -1),

                    Transition('q1', 'q1', '1', '1', '1', 1, -1),
                    Transition('q1', 'q1', '0', '0', '0', 1, -1),
                    Transition('q1', 'q1', '1', '0', '0', 1, -1),
                    Transition('q1', 'q1', '0', '1', '1', 1, -1),

                    Transition('q1', 'q2', '_', 'Z', 'Z', -1, 0),
                    Transition('q1', 'q4', '_', '1', '1', 0, 0),
                    Transition('q1', 'q4', '_', '0', '0', 0, 0),

                    Transition('q2', 'q2', '0', 'Z', 'Z', -1, 0),
                    Transition('q2', 'q2', '1', 'Z', 'Z', -1, 0),

                    Transition('q2', 'q3', '#', 'Z', 'Z', 1, 1),

                    Transition('q3', 'q3', '1', '1', '1', 1, 1),
                    Transition('q3', 'q3', '0', '0', '0', 1, 1),

                    Transition('q3', 'q4', '0', '1', '1', 0, 0)
                    ]

    tm = TM(['q0', 'q1', 'q2', 'q3', 'q4'], 'q0', 'Z', ['q4'], tr_functions)

    pathToInput = "input.txt"
    pathToOutput = "output.txt"

    # For i/o
    sys.stdout = open(pathToOutput, 'w')
    with open(pathToInput, 'r') as file:
        string = file.read()

    match = re.search(r'^(1[01]*|[0]+)#(1[01]*|[0]+)$', string)
    if match is None:
        print('Invalid input')
    else:
        print(('YES' if tm.accept_string(string + '_', pprint=True) else 'NO'))
