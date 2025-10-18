from abc import ABC, abstractmethod
from typing import Union

from src.regular.regular_expression import EmptySet, EmptyString, RegularExpression, Symbol, make_concat, make_kleene_star, make_union

class RegexConvertible:
    """
        Mixin for regex conversion.
    """

    def to_regex(self) -> RegularExpression:
        """
            Convert FSA to a RegEx using state state elimination.

            https://cs.stackexchange.com/questions/130529/complete-explanation-of-state-elimination-methods
        """
        states = self.get_states()

        # R[i][j] - regex for direct transition from state i to state j
        R: dict[str, dict[str, RegularExpression]] = {} # Example: R["S"]["A"] = Symbol("a"), S--a-->A

        for state1 in states:
            R[state1] = {}
            for state2 in states:
                R[state1][state2] = EmptySet()

        for from_state, transitions in self.delta.items():
            for symbol, target in transitions.items():
                if symbol == '':  # Epsilon transition
                    symbol_regex = EmptyString()
                else:
                    symbol_regex = Symbol(symbol)

                if isinstance(self, DFA):
                    # Target is a single state
                    to_state = target
                    curr_symbol = R[from_state][to_state]
                    if isinstance(curr_symbol, EmptySet):
                        R[from_state][to_state] = symbol_regex # No symbols yet
                    else:
                        R[from_state][to_state] = make_union(curr_symbol, symbol_regex)
                else:
                    # Target is a set of state
                    for to_state in target:
                        curr_symbol = R[from_state][to_state]
                        if isinstance(curr_symbol, EmptySet):
                            R[from_state][to_state] = symbol_regex # No symbols yet
                        else:
                            R[from_state][to_state] = make_union(curr_symbol, symbol_regex)

        # One final state for NFAs
        if len(self.final_states) > 1:
            new_final_state = "F_new"
            states.add(new_final_state)
            R[new_final_state] = {}
            for state in states:
                if state != new_final_state:
                    R[state][new_final_state] = EmptySet()
                R[new_final_state][state] = EmptySet()

            # Epsilon transitions
            for final_state in self.finale_states:
                R[final_state][new_final_state] = EmptyString()

            final_state = new_final_state
        else:
            final_state = next(iter(self.final_states))

        # State elimination
        elimination_order = [state for state in states if state not in (self.start, final_state)]

        for k in elimination_order:
            remaining_states = [state for state in states if state != l]

            for i in remaining_states:
                for j in remaining_states:
                    # New path: i -> k -> j
                    # R'[i][j] = R[i][j] | R[i][k] R[k][k]* R[k][j]
                    # R[k][k]* = loop on k
                    old_path = R[i][j]
                    new_path = make_concat(
                        make_concat(R[i][k], make_kleene_star(R[k][k])),
                        R[k][j]
                    )
                    R[i][j] = make_union(old_path, new_path)

            states.remove(k)

        start_loop = R[self.start][self.start]
        direct_path = R[self.start][final_state]

        if isinstance(start_loop, EmptySet):
            return direct_path
        
        return make_concat(make_kleene_star(start_loop), direct_path)


class FSA(ABC):
    """
        Abstract base class for Finite State Automata.

        Default values are derived from one of the homeworks: a DFA accepting 
        strings with an odd number of b's and an even number of a's,
    """

    def __init__(
        self,
        alphabet = None,
        transitions = None,
        start_state = None,
        final_states = None 
    ):
        if alphabet is None:
            self.alphabet = {'a', 'b'}
        else:
            self.alphabet = set(alphabet)

        if start_state is None:
            self.start = 'S'
        else:
            self.start = start_state

        if final_states is None:
            self.final_states = {'F'}
        else:
            self.final_states = set(final_states)

        if transitions is None:
            self.delta = {
                'S': {'a': 'A', 'b': 'F'},
                'A': {'a': 'S', 'b': 'B'},
                'B': {'a': 'F', 'b': 'A'},
                'F': {'a': 'B', 'b': 'S'},
            }
        else:
            self.delta = transitions

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
        if state not in self.delta:
            raise ValueError(f"Unknown state: {state}")
        if symbol not in self.alphabet:
            raise ValueError(f"Symbol '{symbol}' not in alphabet {sorted(self.alphabet)}")
        if symbol not in self.delta[state]:
            raise ValueError(f"No transition from state '{state}' on symbol '{symbol}'")
        return self.delta[state][symbol]

    def accepts(self, s: str) -> bool:
        """
            Return True iff the DFA accepts the string s.
        """
        state = self.state
        for i, ch in enumerate(s):
            if ch not in self.alphabet:
                raise ValueError(f"invalid input symbol at pos {i}: '{ch}' not in alphabet {sorted(self.alphabet)}")
            state = self.step(state, ch)
        return state in self.final_states


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
        super().__init__(alphabet, transitions, start_state, final_states)
        self._normalize_transitions()

    def _normalize_transitions(self):
        """
            Normalize transitions to sets.
        """
        for state in self.delta:
            for symbol in self.delta[state]:
                if not isinstance(self.delta[state][symbol], (set, list)):
                    self.delta[state][symbol] = {self.delta[state][symbol]}
                else:
                    self.delta[state][symbol] = set(self.delta[state][symbol])

    def epsilon_closure(self, states: set[str]) -> set[str]:
        """
            Compute epsilon closure of a set of states using DFS.
        """
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
        """
            Return set of next states.        
        """
        if state not in self.delta:
            return set()
        if symbol not in self.alphabet:
            raise ValueError(f"symbol '{symbol}' not in alphabet {sorted(self.alphabet)}")
        if symbol not in self.delta[state]:
            return set()
        
        return self.delta[state][symbol]
            

    def step_nfa(self, states: set[str], symbol: str) -> set[str]:
        """
            Perform one step on a set of states.
        """
        next_states = set()
        
        for state in states:
            next_states.update(self.step(state, symbol))
        
        return self.epsilon_closure(next_states)

    def accepts(self, s: str) -> str:
        """
            Return True iff the NFA accepts the string s using
        """
        curr_states = self.epsilon_closure({self.start})

        for i, ch in enumerate(s):
            if ch not in self.alphabet:
                raise ValueError(f"invalid input symbol at pos {i}: '{ch}' not in alphabet {sorted(self.alphabet)}")

            curr_states = self.step_nfa(curr_states, ch)

            if not curr_states:
                return False 

        return bool(curr_states & self.final_states)


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
