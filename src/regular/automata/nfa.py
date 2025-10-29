from src.regular.regular_expression import EmptySet, Symbol
from src.regular.fsa_base import FSA
from src.regular.regex_convertible import RegexConvertible

class NFA(FSA, RegexConvertible):
    """
        Non-deterministic Finite Automaton.
    """
    def __init__(self, alphabet=None, transitions=None, start_state=None, final_states=None):
        super().__init__(alphabet, transitions, start_state, final_states)
        self._normalize_transitions()

    def _normalize_transitions(self):
        for state in self.delta:
            for symbol in self.delta[state]:
                if not isinstance(self.delta[state][symbol], (set, list)):
                    self.delta[state][symbol] = {self.delta[state][symbol]}
                else:
                    self.delta[state][symbol] = set(self.delta[state][symbol])

    def epsilon_closure(self, states: set[str]) -> set[str]:
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            if state not in self.delta or '' not in self.delta[state]:
                continue
            for next_state in self.delta[state]['']:
                if next_state in closure:
                    continue
                closure.add(next_state)
                stack.append(next_state)
        return closure

    def step(self, state: str, symbol: str) -> set[str]:
        if state not in self.delta:
            return set()
        if symbol not in self.alphabet:
            raise ValueError(f"symbol '{symbol}' not in alphabet {sorted(self.alphabet)}")
        if symbol not in self.delta[state]:
            return set()
        return self.delta[state][symbol]

    def step_nfa(self, states: set[str], symbol: str) -> set[str]:
        next_states = set()
        for state in states:
            next_states.update(self.step(state, symbol))
        return self.epsilon_closure(next_states)

    def accepts(self, s: str) -> str:
        curr_states = self.epsilon_closure({self.start})
        for i, ch in enumerate(s):
            if ch not in self.alphabet:
                raise ValueError(f"invalid input symbol at pos {i}: '{ch}' not in alphabet {sorted(self.alphabet)}")
            curr_states = self.step_nfa(curr_states, ch)
            if not curr_states:
                return False 
        return bool(curr_states & self.final_states)
