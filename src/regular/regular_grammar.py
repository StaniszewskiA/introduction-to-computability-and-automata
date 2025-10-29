from dataclasses import dataclass
from enum import Enum
from typing import Optional

class GrammarType(Enum):
    RIGHT_LINEAR = "right_linear"
    LEFT_LINEAR = "left_linear"


@dataclass(frozen=True)
class RegularProduction:
    """
        A production rule in a regular grammar.
        
        For right-linear: A → aB, A → a, or A → ε
        For left-linear: A → Ba, A → a, or A → ε
    """
    left_side: str # Non-terminal symbol
    terminal: Optional[str]
    right_side: Optional[str]
    grammar_type: GrammarType

    def __post_init__(self):
        """
            Validate the production rules.
        """
        if self.grammar_type == GrammarType.RIGHT_LINEAR:
            if self.terminal is None and self.right_side is not None:
                raise ValueError("Right-linear grammar cannot have variable without terminal (except ε)")
        elif self.grammar_type == GrammarType.LEFT_LINEAR:
            if self.terminal is None and self.right_side is not None:
                raise ValueError("Left-linear grammar cannot have variable without terminal (except ε)")

    def __str__(self):
        if self.terminal is None and self.right_side is None:
            # epsilon production
            return f"{self.left_side} -> epsilon"
        elif self.terminal is not None and self.right_side is None:
            # terminal production A -> a
            return f"{self.left_side} -> {self.terminal}"
        elif self.grammar_type == GrammarType.RIGHT_LINEAR:
            # right-linear: A -> aB
            return f"{self.left_side} -> {self.terminal}{self.right_side}"
        else:
            # left-linear: A -> Ba
            return f"{self.left_side} -> {self.right_side}{self.terminal}"

    def is_epsilon_production(self) -> bool:
        return self.terminal is None and self.right_side is None

    def is_terminal_production(self) -> bool:
        return self.terminal is not None

    def has_variable(self) -> bool:
        return self.right_side is not None

    @classmethod
    def epsilon_production(cls, left_side: str, grammar_type: GrammarType) -> 'RegularProduction':
        """
            Create an epsilon production: A -> ε
        """
        return cls(left_side, None, None, grammar_type)

    @classmethod 
    def terminal_production(cls, left_side: str, terminal: str, grammar_type: GrammarType) -> 'RegularProduction':
        """
            Create a terminal production: A -> a
        """
        return cls(left_side, terminal, None, grammar_type)

    @classmethod
    def right_linear_production(cls, left_side: str, terminal: str, right_side: str) -> 'RegularProduction':
        """
            Create a right-linear production: A -> aB
        """
        return cls(left_side, terminal, right_side, GrammarType.RIGHT_LINEAR)
        

    @classmethod
    def left_linear_production(cls, left_side: str, terminal: str, right_side: str) -> 'RegularProduction':
        """
            Create a right-linear production: A -> Ba
        """
        return cls(left_side, terminal, right_side, GrammarType.LEFT_LINEAR)


class RegularGrammar:
    """
        Regular Grammar implementation.
        
        Supports both right-linear and left-linear regular grammars.
    """
    def __init__(
        self,
        variables: set[str],
        terminals: set[str],
        productions: list[RegularProduction],
        start_variable: str,
        grammar_type: GrammarType
    ):
        self.variables = variables
        self.terminals = terminals
        self.productions = productions
        self.start_variable = start_variable
        self.grammar_type = grammar_type

        # Validation logic moved from __post_init__ to __init__
        if self.start_variable not in self.variables:
            raise ValueError(
                f"Start variable '{self.start_variable}' must be in variables set!"
            )

        if self.variables & self.terminals:
            raise ValueError(
                f"Variables and terminals sets must be disjoint!"
            )

        for prod in self.productions:
            if prod.left_side not in self.variables:
                raise ValueError(
                    f"Left side '{prod.left_side} must be a variable!"
                )

            if prod.grammar_type != self.grammar_type:
                raise ValueError(
                    f"All productions must be {self.grammar_type.value}!"
                )

            if prod.terminal is not None and prod.terminal not in self.terminals:
                raise ValueError(
                    f"Terminal '{prod.terminal} must be in the terminals set!"
                )

            if prod.right_side is not None and prod.right_side not in self.variables:
                raise ValueError(
                    f"Variable '{prod.right_side} must be in the variables set!"
                )

    def __str__(self) -> str:
        lines: list[str] = []
        lines.append(f"Regular Grammar {self.grammar_type.value}")
        lines.append(f"Variables: {','.join(sorted(self.variables))}")
        lines.append(f"Terminals: {','.join(sorted(self.terminals))}")
        lines.append(f"Start Variables: {self.start_variable}")
        lines.append(f"Productions:")

        for prod in self.productions:
            lines.append(f" {prod}")

        return "\n".join(lines)

    def get_produtions_for_variable(self, variable: str) -> list[RegularProduction]:
        """
            Get all productions with the given variable on the left side.
        """
        return [prod for prod in self.productions if prod.left_side == variable]

    def get_nullable_variables(self) -> set[str]:
        """
            Find all variables that can derive an empty string.
        """
        nullable = set()

        for prod in self.productions:
            if prod.is_epsilon_production():
                nullable.add(prod.left_side)

        return nullable

    def derives_epsilon(self) -> bool:
        """
            Check if the grammar derives an empty string.
        """
        return self.start_variable in self.get_nullable_variables()

    def is_valid_regular_grammar(self) -> bool:
        """
            Verify that all productions follow the regular grammar format.
        """
        try:
            for prod in self.productions:
                if prod.grammar_type != self.grammar_type:
                    return False
                
                if self.grammar_type == GrammarType.RIGHT_LINEAR:
                    if prod.right_side is not None and prod.terminal is None:
                        return False
                elif self.grammar_type == GrammarType.LEFT_LINEAR:
                    if prod.right_side is not None and prod.terminal is None:
                        return False

            return True
        except Exception:
            return False

    def to_finite_automaton(self):
        """
        Convert regular grammar to an NFA compatible with fsa.py's make_nfa.
        """
        from src.regular.fsa import make_nfa

        states = set(self.variables)
        alphabet = set(self.terminals)
        transitions = {v: {} for v in self.variables}
        final_states = set()

        extra_final = None

        for prod in self.productions:
            # A -> ε
            if prod.is_epsilon_production():
                final_states.add(prod.left_side)
            elif prod.grammar_type == GrammarType.RIGHT_LINEAR:
                # A -> aB
                if prod.right_side is not None:
                    transitions[prod.left_side].setdefault(prod.terminal, set()).add(prod.right_side)
                # A -> a
                else:
                    if extra_final is None:
                        extra_final = "[Final]"
                        states.add(extra_final)
                    transitions[prod.left_side].setdefault(prod.terminal, set()).add(extra_final)
                    final_states.add(extra_final)
            elif prod.grammar_type == GrammarType.LEFT_LINEAR:
                # A -> Ba
                if prod.right_side is not None:
                    transitions[prod.right_side].setdefault(prod.terminal, set()).add(prod.left_side)
                # A -> a
                else:
                    if extra_final is None:
                        extra_final = "[FINAL]"
                        states.add(extra_final)
                    transitions[prod.left_side].setdefault(prod.terminal, set()).add(extra_final)
                    final_states.add(extra_final)

        # Normalize transitions
        for state in transitions:
            for symbol in transitions[state]:
                transitions[state][symbol] = set(transitions[state][symbol])

        # Remove empty transitions
        transitions = {
            state: transition 
            for state, transition in transitions.items() 
            if transition
        }

        return make_nfa(
            alphabet=alphabet,
            transitions=transitions,
            start_state=self.start_variable,
            final_states=final_states
        )


def make_regular_grammar(
    variables: set[str] = None,
    terminals: set[str] = None,
    productions: list[RegularProduction] = None,
    start_variable: str = None,
    grammar_type: GrammarType = GrammarType.RIGHT_LINEAR
) -> RegularGrammar:
    """
        Factory method for regular grammars.
    """
    if variables is None:
        variables = set()
    if terminals is None:
        terminals = set()
    if productions is None:
        productions = []
    if start_variable is None and variables:
        start_variable = next(iter(variables))

    return RegularGrammar(variables, terminals, productions, start_variable, grammar_type)


def main():
    grammar = make_regular_grammar(
        variables={'S', 'A'},
        terminals={'0', '1'},
        productions=[
            RegularProduction.right_linear_production('S', '0', 'S'),
            RegularProduction.right_linear_production('S', '1', 'S'),
            RegularProduction.right_linear_production('S', '0', 'A'),
            RegularProduction.terminal_production('A', '1', GrammarType.RIGHT_LINEAR)
        ],
        start_variable='S',
        grammar_type=GrammarType.RIGHT_LINEAR
    )

    print(grammar)


if __name__ == "__main__":
    main()
