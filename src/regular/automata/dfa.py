from src.regular.regular_expression import EmptySet, Symbol, make_union
from src.regular.fsa_base import FSA
from src.regular.regex_convertible import RegexConvertible

class DFA(FSA, RegexConvertible):
    """
        Deterministic Finite Automaton.
    """
    def step(self, state: str, symbol: str) -> str:
        if state not in self.delta:
            raise ValueError(f"Unknown state: {state}")
        if symbol not in self.alphabet:
            raise ValueError(f"Symbol '{symbol}' not in alphabet {sorted(self.alphabet)}")
        if symbol not in self.delta[state]:
            raise ValueError(f"No transition from state '{state}' on symbol '{symbol}'")
        return self.delta[state][symbol]

    def accepts(self, s: str) -> bool:
        state = self.start
        for i, ch in enumerate(s):
            if ch not in self.alphabet:
                raise ValueError(f"invalid input symbol at pos {i}: '{ch}' not in alphabet {sorted(self.alphabet)}")
            state = self.step(state, ch)
        return state in self.final_states
