from src.regular.fsa_base import FSA

class MealyMachine(FSA):
    """
        Mealy Machine
    """
    def __init__(
        self, 
        alphabet=None, 
        transitions=None, 
        start_state=None,
        output=None 
    ):
        super().__init__(alphabet, transitions, start_state)
        if output is None:
            self.output = {state: "" for state in self.get_states()}
        else:
            self.output = dict(output)

    def get_output(self, state: str) -> str:
        """
            Get output for a given state.
        """
        return self.output.get(state, "")

    def step(self, state: str, symbol: str) -> tuple[str, str]:
        """
            Return the next state and the output symbol
        """
        if state not in self.delta:
            raise ValueError(f"Unknown state: {state}")
        if symbol not in self.alphabet:
            raise ValueError(f"Symbol '{symbol}' not in alphabet {sorted(self.alphabet)}")
        if symbol not in self.delta[state]:
            raise ValueError(f"No transition from state '{state}' on symbol '{symbol}'")
        
        next_state = self.delta[state][symbol]
        output_symbol = self.get_output(state, symbol)

        return next_state, output_symbol
    
    def get_output(self, state: str, symbol: str) -> str:
        """
            Get output for a given state and input symbol.
            Overrides defualt FSA implementation.
        """
        return self.output.get(state, {}).get(symbol, "")

    def process_input(self, input_str: str) -> list[str]:
        """
            Process input string and return list of outputs.
        """
        outputs = []
        state = self.start

        for symbol in input_str:
            state, output_symbol = self.step(state, symbol)
            outputs.append(output_symbol)

        return outputs
    
    def accepts(self, string: str) -> bool:
        """
            Placeholder: Mealy Machines are not acceptors
        """
        raise NotImplementedError("Moore Machines are not acceptors")
