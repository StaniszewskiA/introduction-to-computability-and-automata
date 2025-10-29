import pytest
from src.regular.regular_grammar import RegularGrammar, RegularProduction, GrammarType, make_regular_grammar

# =============================================================================
# BASIC REGULAR GRAMMAR FUNCTIONALITIES
# =============================================================================
class TestRegularGrammarBasicFunctionalities:
    """
        Class for basic regular grammar functionalities.
    """
    def test_str_repr(self):
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

        grammar_str = str(grammar)

        assert 'Regular Grammar' in grammar_str
        assert 'Variables:' in grammar_str
        assert 'Terminals:' in grammar_str
        assert 'Productions:' in grammar_str
        assert 'S -> 0S' in grammar_str or 'S -> S0' in grammar_str

    def test_epsilon_and_terminal_productions(self):
        prod_eps = RegularProduction.epsilon_production('A', GrammarType.RIGHT_LINEAR)
        prod_term = RegularProduction.terminal_production('A', '1', GrammarType.RIGHT_LINEAR)

        assert prod_eps.is_epsilon_production()
        assert prod_term.is_terminal_production()

        assert not prod_eps.is_terminal_production()
        assert not prod_term.is_epsilon_production()

    def test_invalid_grammar_type(self):
        with pytest.raises(ValueError):
            RegularProduction('A', None, 'B', GrammarType.RIGHT_LINEAR)
        with pytest.raises(ValueError):
            RegularProduction('A', None, 'B', GrammarType.LEFT_LINEAR)

    def test_grammar_validation(self):
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

        assert grammar.is_valid_regular_grammar()

    def test_invalid_start_variable(self):
        with pytest.raises(ValueError):
            RegularGrammar({'S', 'A'}, {'0', '1'}, [], 'B', GrammarType.RIGHT_LINEAR)

    def test_disjoint_variables_terminals(self):
        with pytest.raises(ValueError):
            RegularGrammar({'S', 'A', '0'}, {'0', '1'}, [], 'S', GrammarType.RIGHT_LINEAR)

    def test_invalid_production_left_side(self):
        with pytest.raises(ValueError):
            RegularGrammar(
                {'S', 'A'}, 
                {'0', '1'}, 
                [
                    RegularProduction.right_linear_production('B', '0', 'S')
                ], 
                'S', 
                GrammarType.RIGHT_LINEAR
            )

    def test_invalid_production_terminal(self):
        with pytest.raises(ValueError):
            RegularGrammar(
                {'S', 'A'},
                {'0', '1'},
                [
                    RegularProduction.right_linear_production('S', '2', 'A')
                ],
                'S',
                GrammarType.RIGHT_LINEAR
            )

    def test_invalid_production_right_side(self):
        with pytest.raises(ValueError):
            RegularGrammar(
                {'S', 'A'},
                {'0', '1'},
                [
                    RegularProduction.right_linear_production('S', '0', 'B')
                ],
                'S',
                GrammarType.RIGHT_LINEAR
            )

# =============================================================================
# REGULAR GRAMMAR TO AUTOMATON CONVERSION
# =============================================================================
class TestRegularGrammarToAutomaton:
    """
        Class for regular grammar to automaton tests.
    """
    def test_converted_automaton_accepts(self):
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

        nfa = grammar.to_finite_automaton()
        assert nfa.accepts('01')
        assert nfa.accepts('001')
        assert not nfa.accepts('10')
        assert not nfa.accepts('')

    def test_converted_automaton_epsilon(self):
        grammar = make_regular_grammar(
            variables={'S'},
            terminals={'a'},
            productions=[
                RegularProduction.epsilon_production('S', GrammarType.RIGHT_LINEAR)
            ],
            start_variable='S',
            grammar_type=GrammarType.RIGHT_LINEAR
        )

        nfa = grammar.to_finite_automaton()
        assert nfa.accepts('')
        assert not nfa.accepts('a')

# =============================================================================
# LEFT-LINEAR GRAMMAR
# =============================================================================
# TODO
