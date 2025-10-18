from abc import ABC, abstractmethod
from typing import Union

from src.regular.regular_expression import RegularExpression

class RegexConvertible:
    """
        Mixin for regex conversion between DFA and NFA.
    """

    def to_regex(self) -> RegularExpression:
        """
            Convert FSA to a RegEx using state state elimination.
        """
        pass


class FSA(ABC):
    """
        Abstract base class for Finite State Automata.
    """

    def __init__(
        self,
        alphabet = None,
        transitions = None,
        start_state = None,
        final_states = None 
    ):
        pass

    @abstractmethod
    def accepts(self, s: str) -> bool:
        """
            Return true iff the FSA accepts the string s.
        """
        pass

    @abstractmethod
    def step(self, state: str, symbol: str) -> Union[str, set[str]]:
        """
            Perform one step in the computation.
        """
        pass

    def get_states(self) -> set[str]:
        """
            Return all states in the automaton.
        """
        return set(self.delta.keys())
    

class DFA(FSA, RegexConvertible):
    """
        Deterministic Finite Automaton.
    """

    def step(self, state: str, symbol: str) -> str:
        """
            Return next state from state on input symbol.
        """
        pass

    def accepts(self, s: str) -> bool:
        """
            Return True iff the DFA accepts the string s.
        """
        pass


class NFA(FSA, RegexConvertible):
    """
        Non-deterministic Finite Automaton.
    """

    def __init__(
        self, 
        alphabet = None, 
        transitions = None, 
        start_state = None, 
        final_states = None
    ):
        pass

    def _normalize_transition(self):
        """
            Normalize transitions to sets.
        """
        pass

    def epsilon_closure(self, states: set[str]) -> set[str]:
        """
            Compute epsilon closure of a set of states.
        """
        pass

    def step(self, state: str, symbol: str) -> set[str]:
        """
            Return set of next states.        
        """
        pass

    def step_nfa(self, states: set[str], symbol: str) -> set[str]:
        """
            Perform one step on a set of states.
        """
        pass

    def accepts(self, s: str) -> str:
        """
            Return True iff the NFA accepts the string s using
        """
        pass


def make_fsa(alphabet = None, transitions = None, state_state = None, final_states = None, is_deterministic = True) -> FSA:
    """
        FSA factory.
    """
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
