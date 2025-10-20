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
    grammar_Type: GrammarType

    def __post_init__(self):
        """
            Validate the production rules.
        """
        pass

    def __str__(self):
        pass

    def is_epsilon_production(self) -> bool:
        pass

    def is_terminal_production(self) -> bool:
        pass

    def has_variable(self) -> bool:
        pass

    @classmethod
    def epsilon_production(cls, left_side: str, grammar_type: GrammarType) -> 'RegularProduction':
        pass

    @classmethod 
    def terminal_production(cls, left_side: str, terminal: str, grammar_type: GrammarType) -> 'RegularProduction':
        pass

    @classmethod
    def right_linear_production(cls, left_side: str, terminal: str, right_side: str) -> 'RegularProduction':
        pass

    @classmethod
    def left_linear_production(Cls, left_side: str, terminal: str, right_side: str) -> 'RegularProduction':
        pass


class RegularGrammar:
    """
        Regular Grammar implementation.
        
        Supports both right-linear and left-linear regular grammars.
    """
    



def make_regular_grammar(
    variables: set[str] = None,
    terminals: set[str] = None,
    productions: list[RegularProduction] = None,
    start_variable: str = None,
    grammar_type: GrammarType = GrammarType.RIGHT_LINEAR
):
    """
        Regular grammar factory.
    """
    def __init__(
        self,
        variables: set[str],
        terminals: set[str],
        productions: list[RegularProduction],
        start_variable: str,
        grammar_type: GrammarType
    ):
        pass

    def __str__(self) -> str:
        pass

    def get_produtions_for_variable(self, variable: str) -> list[RegularProduction]:
        pass

    def get_nullable_variables(self) -> set[str]:
        pass

    def derives_epsilon(self) -> bool:
        pass

    def to_finite_automaton(self):
        pass


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
    pass
