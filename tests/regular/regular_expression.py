import pytest
from src.regular.regular_expression import (
    RegularExpression, Symbol, EmptyString, EmptySet, RegexUnion, RegexConcat, RegexKleeneStar, make_union, make_concat, make_kleene_star
)


class TestSymbol:
    """
        Class for Symbol tests.
    """
    
    def test_symbol_creation(self):
        a = Symbol('a')
        assert str(a) == 'a'
        assert a.symbol == 'a'

    def test_symbol_equality(self):
        a1 = Symbol('a')
        a2 = Symbol('a')
        b = Symbol('b')

        assert a1 == a2
        assert a1 != b
        assert a1 != 'a' # Typing error expected

    def test_symbol_repr(self):
        a = Symbol('a')
        assert repr(a) == "Symbol(a)"

    def test_symbol_various_chars(self):
        symbols = ['0', '1', 'x', '@', '_']
        for char in symbols:
            s = Symbol(char)
            assert str(s) == char
            assert s.symbol == char


class TestEmptySymbol:
    """
        Class for EmptyString (epsilon) tests.
    """

    def test_empty_symbol_creation(self):
        eps = EmptyString()
        assert str(eps) == 'ε'
        assert str(eps) == "\u03b5"

    def test_empty_symbol_equality(self):
        eps1 = EmptyString()
        eps2 = EmptyString()
        
        assert eps1 == eps2
        assert eps1 != Symbol('a')

    def test_empty_symbol_repr(sself):
        eps = EmptyString()
        assert repr(eps) == "EmptyString(ε)"


class TestEmptySet:
    """
        Class for EmptySet tests.
    """

    def test_empty_set_creation(self):
        empty = EmptySet()
        assert str(empty) == '∅'
        assert str(empty) == "\u2205"

    def test_empty_set_equality(self):
        empty1 = EmptySet()
        empty2 = EmptySet()

        assert empty1 == empty2
        assert empty1 != Symbol('a')
        assert empty1 != EmptyString()

    def test_empty_set_repr(self):
        empty = EmptySet()
        assert repr(empty) == "EmptySet(∅)"


class TestRegexUnion:
    """
        Class for regex union tests.
    """

    def test_regex_union_creation(self):
        a = Symbol('a')
        b = Symbol('b')
        union = RegexUnion(a, b)

        assert union.left == a
        assert union.right == b

    def test_regex_union_rep(self):
        a = Symbol('a')
        b = Symbol('b')
        union = RegexUnion(a, b)

        res = str(union)
        assert '(a|b)' == res or '(b|a)' == res

    def test_regex_union_with_empty_set(self):
        a = Symbol('a')
        empty = EmptySet()

        union1 = RegexUnion(empty, a)
        assert str(union1) == 'a'

        union2 = RegexUnion(a, empty)
        assert str(union2) == 'a'

    def test_union_same_operands(self):
        a = Symbol('a')
        union = RegexUnion(a, a)
        assert str(union) == 'a'

    def test_nested_regex_union_parentheses(self):
        a = Symbol('a')
        b = Symbol('b')
        c = Symbol('c')

        inner_union = RegexUnion(a, b)
        outer_union = RegexUnion(inner_union, c)

        res = str(outer_union)
        assert res.count('(') <= 1


class TestRegexConcat:
    """
        Class for regex concatenation tests.
    """

    def test_concat_creation(self):
        a = Symbol('a')
        b = Symbol('b')
        concat = RegexConcat(a, b)

        assert concat.left == a
        assert concat.right == b

    def test_concat_string_repr(self):
        a = Symbol('a')
        b = Symbol('b')
        concat = RegexConcat(a, b)

        assert str(concat) == "ab"

    def test_concat_with_empty_string(self):
        a = Symbol('a')
        eps = EmptyString()

        concat1 = RegexConcat(eps, a)
        assert str(concat1) == 'a'

        concat2 = RegexConcat(a, eps)
        assert str(concat2) == 'a'

    def test_concat_with_empty_set(self):
        a = Symbol('a')
        empty = EmptySet()

        concat1 = RegexConcat(empty, a)
        assert str(concat1) == '∅'
        assert str(concat1) == "\u2205"

        concat2 = RegexConcat(a, empty)
        assert str(concat2) == '∅'
        assert str(concat2) == "\u2205"

    def test_concat_with_union_add_parentheses(self):
        a = Symbol('a')
        b = Symbol('b')
        c = Symbol('c')

        union = RegexUnion(a, b)
        concat = RegexConcat(union, c)

        res = str(concat)
        assert res.startswith('(') and '|' in res and res.endswith('c')


class TestRegexKleeneStar:
    """
        Class for regex Kleene Star tests.
    """

    def test_kleene_star_creation(self):
        a = Symbol('a')
        star = RegexKleeneStar(a)

        assert star.expr == a
        assert str(star) == "a*"

    def test_kleene_star_empty(self):
        eps = EmptyString()
        star = RegexKleeneStar(eps)

        # ε* = ε
        assert str(star) == 'ε'
        assert str(star) == "\u03b5"

    def test_kleene_start_empty_set(self):
        empty = EmptySet()
        star = RegexKleeneStar(empty)

        # ∅* = ε
        assert str(star) == 'ε'
        assert str(star) == "\u03b5"

    def test_kleene_star_union_parentheses(self):
        a = Symbol('a')
        b = Symbol('b')

        union = RegexUnion(a, b)
        star = RegexKleeneStar(union)

        res = str(star)

        assert res.startswith('(') and '|' in res and res.endswith(')*')

    def test_start_with_concat_parentheses(self):
        a = Symbol('a')
        b = Symbol('b')

        concat = RegexConcat(a, b)
        star = RegexKleeneStar(concat)

        res = str(star)
        assert res == '(ab)*'

    def test_start_epsilon_union(self):
        a = Symbol('a')
        eps = EmptyString()

        union1 = RegexUnion(eps, a)
        star1 = RegexKleeneStar(union1)
        assert str(star1) == "a*"

        union2 = RegexUnion(a, eps)
        star2 = RegexKleeneStar(union2)
        assert str(star2) == "a*"


class TestFactoryFunctions:
    """
        Class for regex factory functions tests.
    """
    
    def test_make_union(self):
        a = Symbol('a')
        b = Symbol('b')
        empty = EmptySet()

        union = make_union(a, b)
        assert isinstance(union, RegexUnion)

        assert make_union(empty, a) == a
        assert make_union(a, empty) == a
        assert make_union(a, a) == a

    def test_make_concat(self):
        a = Symbol('a')
        b = Symbol('b')
        eps = EmptyString()
        empty = EmptySet()
        
        concat = make_concat(a, b)
        assert isinstance(concat, RegexConcat)
        
        assert make_concat(eps, a) == a
        assert make_concat(a, eps) == a
        assert isinstance(make_concat(empty, a), EmptySet)
        assert isinstance(make_concat(a, empty), EmptySet)

    def test_make_kleene_star(self):
        a = Symbol('a')
        eps = EmptyString()
        empty = EmptySet()

        star = make_kleene_star(a)
        assert isinstance(star, RegexKleeneStar)

        eps_star = make_kleene_star(eps)
        assert isinstance(eps_star, EmptyString)

        empty_star = make_kleene_star(empty)
        assert isinstance(empty_star, EmptyString)


class TestComplexExpressions:
    """
        Class for complex regex tests.
    """

    def test_nested_expressions(self):
        a = Symbol('a')
        b = Symbol('b')

        # (a|b)*
        union = make_union(a, b)
        star = make_kleene_star(union)

        res = str(star)
        assert '(' in res and '|' in res and res.endswith(')*')

    def test_mixed_operations(self):
        a = Symbol('a')
        b = Symbol('b')
        c = Symbol('c')

        # a(b|c)*
        union = make_union(b, c)
        star = make_kleene_star(union)
        concat = make_concat(a, star)

        res = str(concat)
        assert res.startswith('a')
        assert '|' in res
        assert res.endswith(')*')

    def test_chain_simplification(self):
        a = Symbol('a')
        eps = EmptyString()
        empty = EmptySet()

        union = make_union(empty, eps)
        assert isinstance(union, EmptyString)

        star = make_kleene_star(union)
        assert isinstance(star, EmptyString)

        concat = make_concat(a, star)
        assert concat == a or str(concat) == 'a'
