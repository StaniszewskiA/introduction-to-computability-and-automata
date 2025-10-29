from abc import ABC, abstractmethod

class FSA(ABC):
    def __init__(self, alphabet=None, transitions=None, start_state=None, final_states=None):
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
        pass

    @abstractmethod
    def step(self, state: str, symbol: str):
        pass

    def get_states(self) -> set[str]:
        return set(self.delta.keys())
