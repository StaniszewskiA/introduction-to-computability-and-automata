from src.regular.fsa_base import FSA

class MooreMachine(FSA):
    """
        Moore Machine: output depends only on the current state.
    """
    def __init__(self, alphabet=None, transitions=None, start_state=None, final_states=None, output=None):
        super().__init__(alphabet, transitions, start_state, final_states)
        if output is None:
            self.output = {state: None for state in self.get_states()}
        else:
            self.output = dict(output)

    def get_output(self, state: str) -> str:
        return self.output.get(state, None)

    def step(self, state: str, symbol: str) -> str:
        if state not in self.delta:
            raise ValueError(f"Unknown state: {state}")
        if symbol not in self.alphabet:
            raise ValueError(f"Symbol '{symbol}' not in alphabet {sorted(self.alphabet)}")
        if symbol not in self.delta[state]:
            raise ValueError(f"No transition from state '{state}' on symbol '{symbol}'")
        return self.delta[state][symbol]

    def process(self, input_str: str) -> list[str]:
        state = self.start
        outputs = [self.get_output(state)]
        for symbol in input_str:
            state = self.step(state, symbol)
            outputs.append(self.get_output(state))
        return outputs

    def accepts(self, s: str) -> bool:
        state = self.start
        for symbol in s:
            state = self.step(state, symbol)
        return state in self.final_states
