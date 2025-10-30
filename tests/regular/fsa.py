import pytest

from src.regular.fsa import make_dfa, make_mealy_machine, make_moore_machine, make_nfa
from src.regular.regular_expression import EmptyString, RegexUnion, RegularExpression, Symbol

@pytest.fixture
def simple_dfa():
    return make_dfa(
        alphabet = {'a', 'b'},
        transitions = {
            'q00': {'a': 'q10', 'b': 'q01'},  # (even_a, even_b) -> (odd_a, even_b) or (even_a, odd_b)
            'q01': {'a': 'q11', 'b': 'q00'},  # (even_a, odd_b) -> (odd_a, odd_b) or (even_a, even_b)  
            'q10': {'a': 'q00', 'b': 'q11'},  # (odd_a, even_b) -> (even_a, even_b) or (odd_a, odd_b)
            'q11': {'a': 'q01', 'b': 'q10'}   # (odd_a, odd_b) -> (even_a, odd_b) or (odd_a, even_b)
        },
        start_state = 'q00',
        final_states = {'q01'}  # even_a AND odd_b
    ) 

@pytest.fixture
def simple_nfa():
    return make_nfa(
        alphabet = {'a', 'b'},
        transitions = {
            'q00': {'a': {'q10'}, 'b': {'q01'}},      # (even_a, even_b) -> (odd_a, even_b) or (even_a, odd_b)
            'q01': {'a': {'q11'}, 'b': {'q00'}},      # (even_a, odd_b) -> (odd_a, odd_b) or (even_a, even_b)  
            'q10': {'a': {'q00'}, 'b': {'q11'}},      # (odd_a, even_b) -> (even_a, even_b) or (odd_a, odd_b)
            'q11': {'a': {'q01'}, 'b': {'q10'}}       # (odd_a, odd_b) -> (even_a, odd_b) or (odd_a, even_b)
        },
        start_state = 'q00',
        final_states = {'q01'}  # even_a AND odd_b
    )

@pytest.fixture
def epsilon_nfa():
    return make_nfa(
        alphabet = {'a', 'b'},
        transitions = {
            'q0': {'': {'q1'}, 'a': {'q0'}},  
            'q1': {'b': {'q2'}},
            'q2': {'': {'q0'}}
        },
        start_state = 'q0',
        final_states = {'q2'}
    )

@pytest.fixture
def multi_final_nfa():
    return make_nfa(
        alphabet = {'0', '1'},
        transitions = {
            'q0': {'0': {'q1'}, '1': {'q2'}},
            'q1': {'0': {'q0'}, '1': {'q1'}},
            'q2': {'0': {'q2'}, '1': {'q0'}}
        },
        start_state = 'q0',
        final_states = {'q1', 'q2'}
    )

@pytest.fixture
def simple_moore_machine():
    return make_moore_machine(
        alphabet = {'0', '1'},
        transitions = {
            'S': {'0': 'A', '1': 'B'},
            'A': {'0': 'S', '1': 'B'},
            'B': {'0': 'B', '1': 'S'}
        },
        start_state = 'S',
        output = {
            'S': 'x',
            'A': 'y',
            'B': 'z',
        }        
    )

@pytest.fixture
def simple_mealy_machine():
    return make_mealy_machine(
        alphabet = {'0', '1'},
        transitions = {
            'S': {'0': 'A', '1': 'B'},
            'A': {'0': 'S', '1': 'B'},
            'B': {'0': 'B', '1': 'S'}
        },
        start_state = 'S',
        output = {
            'S': {'0': 'x', '1': 'y'},
            'A': {'0': 'z', '1': 'w'},
            'B': {'0': 'p', '1': 'q'}
        }
    )

# =============================================================================
# BASIC FSA FUNCTIONALITIES
# =============================================================================

class TestBasicFSAFunctionalities:
    """
    Tests for basic FSA functionality that apply to both DFA and NFA.
    """
    
    @pytest.mark.parametrize("automaton", ["simple_dfa", "simple_nfa"])
    def test_fsa_empty_rejected(self, automaton, request):
        fsa = request.getfixturevalue(automaton)
        assert not fsa.accepts('')

    @pytest.mark.parametrize("automaton", ["simple_dfa", "simple_nfa"])
    def test_fsa_single_b_accepted(self, automaton, request):
        fsa = request.getfixturevalue(automaton)
        assert fsa.accepts('b')

    @pytest.mark.parametrize("automaton", ["simple_dfa", "simple_nfa"])
    def test_fsa_single_a_rejected(self, automaton, request):
        fsa = request.getfixturevalue(automaton)
        assert not fsa.accepts('a')

    @pytest.mark.parametrize("automaton", ["simple_dfa", "simple_nfa"])
    def test_fsa_short_string(self, automaton, request):
        fsa = request.getfixturevalue(automaton)
        for s in ("aa", "ab", "ba", "bb"):
            assert not fsa.accepts(s), f"{s} should be rejected by {automaton}"

        accepted = ["aab", "aba", "baa", "bbb"]
        for s in accepted:
            assert fsa.accepts(s), f"{s} should be accepted by {automaton}"

    @pytest.mark.parametrize("automaton", ["simple_dfa", "simple_nfa"])
    def test_fsa_invalid_symbol_raises(self, automaton, request):
        fsa = request.getfixturevalue(automaton)
        with pytest.raises(ValueError):
            fsa.accepts('c')

    @pytest.mark.parametrize("automaton", ["simple_dfa", "simple_nfa"])
    def test_fsa_to_regex_return_regex(self, automaton, request):
        fsa = request.getfixturevalue(automaton)
        regex = fsa.to_regex()
        assert isinstance(regex, RegularExpression)

    @pytest.mark.parametrize("automaton", ["simple_dfa", "simple_nfa"])
    def test_fsa_regex_conversion_string_compatibility(self, automaton, request):
        fsa = request.getfixturevalue(automaton)
        regex = fsa.to_regex()
        regex_str = str(regex)
        assert isinstance(regex_str, str)
        assert len(regex_str) > 0

    def test_regex_basic_functionality(self):
        a = Symbol('a')
        assert str(a) == 'a'

        eps = EmptyString()
        assert str(eps) == "\u03b5"

        union = RegexUnion(Symbol('a'), Symbol('b'))
        assert 'a' in str(union) and 'b' in str(union)

# =============================================================================
# NFA SPECIFIC FUNCTIONALITIES
# =============================================================================

class TestNFASpecificFunctionalities:
    """
    Tests for NFA-specific functionalities.
    """
    
    def test_nfa_epsilon_closure(self, epsilon_nfa):
        closure_q0 = epsilon_nfa.epsilon_closure({'q0'})
        assert 'q0' in closure_q0
        assert 'q1' in closure_q0

        closure_q1 = epsilon_nfa.epsilon_closure({'q1'})
        assert closure_q1 == {'q1'}

        closure_q2 = epsilon_nfa.epsilon_closure({'q2'})
        assert 'q0' in closure_q2
        assert 'q1' in closure_q2
        assert 'q2' in closure_q2

    def test_epsilon_nfa_acceptance(self, epsilon_nfa):
        """Test NFA with epsilon transitions."""
        # Empty string: q0 -ε-> q1, no 'b' transition from q1, so reject
        assert epsilon_nfa.accepts('') == False
        
        # 'b': q0 -ε-> q1 -b-> q2 (accept)
        assert epsilon_nfa.accepts('b') == True
        
        # 'a': q0 -a-> q0, still in q0 (reject)
        assert epsilon_nfa.accepts('a') == False
        
        # 'ab': q0 -a-> q0 -ε-> q1 -b-> q2 (accept)
        assert epsilon_nfa.accepts('ab') == True
        
        # 'bb': q0 -ε-> q1 -b-> q2 -ε-> q0 -ε-> q1 -b-> q2 (accept)
        assert epsilon_nfa.accepts('bb') == True
        
        # 'aab': q0 -a-> q0 -a-> q0 -ε-> q1 -b-> q2 (accept)
        assert epsilon_nfa.accepts('aab') == True

    def test_nfa_multi_final_state(self, multi_final_nfa):
        # Empty string should be rejected
        assert multi_final_nfa.accepts('') == False
        
        # Single '0': q0 -0-> q1 (final state, accept)
        assert multi_final_nfa.accepts('0') == True
        
        # Single '1': q0 -1-> q2 (final state, accept)  
        assert multi_final_nfa.accepts('1') == True
        
        # '00': q0 -0-> q1 -0-> q0 (not final, reject)
        assert multi_final_nfa.accepts('00') == False
        
        # '11': q0 -1-> q2 -1-> q0 (not final, reject)
        assert multi_final_nfa.accepts('11') == False
        
        # '01': q0 -0-> q1 -1-> q1 (final state, accept)
        assert multi_final_nfa.accepts('01') == True
        
        # '10': q0 -1-> q2 -0-> q2 (final state, accept)
        assert multi_final_nfa.accepts('10') == True

    def test_nfa_step_function(self, simple_nfa):
        # From q00 on 'a' - should go to q10 (even_a -> odd_a)
        next_states = simple_nfa.step('q00', 'a')
        assert next_states == {'q10'}
        
        # From q00 on 'b' - should go to q01 (even_b -> odd_b)
        next_states = simple_nfa.step('q00', 'b')
        assert next_states == {'q01'}
        
        # From q01 on 'a' - should go to q11 (even_a -> odd_a)
        next_states = simple_nfa.step('q01', 'a')
        assert next_states == {'q11'}
        
        # From q01 on 'b' - should go to q00 (odd_b -> even_b)
        next_states = simple_nfa.step('q01', 'b')
        assert next_states == {'q00'}

    def test_nfa_step_nfa_function(self, simple_nfa):
        """Test step_nfa function that handles sets of states."""
        # From {q00} on 'a' -> {q10}
        next_states = simple_nfa.step_nfa({'q00'}, 'a')
        assert next_states == {'q10'}
        
        # From {q00, q01} on 'b' -> {q01, q00}
        next_states = simple_nfa.step_nfa({'q00', 'q01'}, 'b')
        assert 'q01' in next_states  # q00 -b-> q01
        assert 'q00' in next_states  # q01 -b-> q00

    def test_nfa_normalization(self):
        nfa = make_nfa(
            alphabet={'a', 'b'},
            transitions={
                'q0': {'a': 'q1', 'b': {'q0', 'q1'}},  # Mixed: string and set
                'q1': {'a': ['q2'], 'b': 'q0'}         # Mixed: list and string
            },
            start_state='q0',
            final_states={'q2'}
        )

        assert isinstance(nfa.delta['q0']['a'], set)
        assert isinstance(nfa.delta['q0']['b'], set)
        assert isinstance(nfa.delta['q1']['a'], set)
        assert isinstance(nfa.delta['q1']['b'], set)
        
        assert nfa.accepts('a') == False
        assert nfa.accepts('aa') == True

# =============================================================================
# MOORE MACHINE FUNCTIONALITIES
# =============================================================================

class TestMooreMachine:
    """
        Tests for Moore Machine functionalities.
    """
    def test_outputs_for_input(self, simple_moore_machine):
        # S --0--> A --1--> B
        # x --0--> y --1--> z
        outputs = simple_moore_machine.process_input("01")
        assert outputs == ['x', 'y', 'z']

    def test_invalid_symbol(self, simple_moore_machine):
        with pytest.raises(ValueError):
            simple_moore_machine.process_input("2")

    def test_output_for_unknown_state(self, simple_moore_machine):
        assert simple_moore_machine.get_output("Q") == ""

    def test_accepts_attempt_fails(self, simple_moore_machine):
        # Moore machines are not acceptors
        with pytest.raises(NotImplementedError):
            assert simple_moore_machine.accepts("01")

# =============================================================================
# MEALY MACHINE FUNCTIONALITIES
# =============================================================================

class TestMealyMachine:
    """
        Tests for Mealy Machine functionalities.
    """
    def test_outputs_for_input(self, simple_mealy_machine):
        # S--0/x--> A --1/w--> b
        outputs = simple_mealy_machine.process_input("01")
        assert outputs == ['x', 'w']

    def test_invalid_symbol(self, simple_mealy_machine):
        with pytest.raises(ValueError):
            simple_mealy_machine.process_input("2")

    def test_out_for_unknown_state(self, simple_mealy_machine):
        assert simple_mealy_machine
