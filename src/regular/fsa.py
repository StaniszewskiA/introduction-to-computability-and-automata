from src.regular.fsa_base import FSA
from src.regular.automatons.dfa import DFA
from src.regular.automatons.nfa import NFA


# Factories
def make_fsa(alphabet=None, transitions=None, state_state=None, final_states=None, is_deterministic=True) -> FSA:
    if is_deterministic:
        return DFA(alphabet, transitions, state_state, final_states)
    else:
        return NFA(alphabet, transitions, state_state, final_states)


def make_dfa(alphabet = None, transitions = None, start_state = None, final_states = None) -> DFA:
    """
        DFA factory.
    """
    return DFA(alphabet, transitions, start_state, final_states)


def make_nfa(alphabet = None, transitions = None, start_state = None, final_states = None) -> NFA:
    """
        NFA factory.
    """
    return NFA(alphabet, transitions, start_state, final_states)
