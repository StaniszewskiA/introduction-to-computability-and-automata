from src.regular.fsa_base import FSA


class MooreMachine(FSA):
    """
        Moore Machine
    """
    def __init__(
        self,
        alphabet=None,
        transitions=None,
        start_state=None,
        final_states=None,
        output=None
    ):
        super().__init__(alphabet, transitions, start_state, final_states)
        if output is None:
            self.output = {state: "" for state in self.get_states()}
        else:
            self.output = dict(output)

    def get_output(self, state: str) -> str:
        """
            Get output for a given state.
        """
        return self.output.get(state, "")

    def step(self, state: str, symbol: str) -> str:
        """
            Return the next state.
        """
        if state not in self.delta:
            raise ValueError(f"Unknown state: {state}")
        if symbol not in self.alphabet:
            raise ValueError(f"Symbol '{symbol}' not in alphabet {sorted(self.alphabet)}")
        if symbol not in self.delta[state]:
            raise ValueError(f"No transition from state '{state}' on symbol '{symbol}'")
        return self.delta[state][symbol]

    def process_input(self, input_str: str) -> list[str]:
        """
            Process input string and return list of outputs.
        """
        outputs = [self.get_output(self.start)]
        state = self.start

        for symbol in input_str:
            state = self.step(state, symbol)
            outputs.append(self.get_output(state))

        return outputs

    def accepts(self, string: str) -> bool:
        """
            Check whether the Moore machine accepts given string.
        """
        state = self.start

        for symbol in string:
            state = self.step(state, symbol)

        return state in self.final_states
        