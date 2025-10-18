"""
Regular expression classes
"""
from abc import ABC, abstractmethod

class RegularExpression(ABC):
    """
        Abstract class for regexes
    """

    @abstractmethod
    def __str__(self):
        pass
    
    def __repr__(self):
        return f"{self.__class__.__name__}({str(self)})"
    

class Symbol(RegularExpression):
    """
        Single terminal symbol
    """

    def __init__(self, symbol: str):
        self.symbol = symbol

    def __str__(self):
        return self.symbol
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Symbol) and self.symbol == other.symbol
    

class EmptyString(RegularExpression):
    """
        Empty string (epsilon)
    """

    def __str__(self) -> str:
        return "\u03b5"  # Unicode for ε
    
    def __eq__(self, other) -> bool:
        return isinstance(other, EmptyString)
    

class EmptySet(RegularExpression):
    """
        Empty set (∅) - accepts nothing.
    """

    def __str__(self) -> str:
        return "\u2205"  # Unicode for ∅
    
    def __eq__(self, other) -> bool:
        return isinstance(other, EmptySet)


class RegexUnion(RegularExpression):
    """
        RegexUnion of two expressions (L_1|L_2)
    """

    def __init__(self, left: RegularExpression, right: RegularExpression):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        if isinstance(self.left, EmptySet):
            return str(self.right)
        if isinstance(self.right, EmptySet):
            return str(self.left)
        if self.left == self.right:
            return str(self.left)
        
        left_str = _strip_parantheses(str(self.left))
        right_str = _strip_parantheses(str(self.right))

        return f"({left_str}|{right_str})"


def make_union(left: RegularExpression, right: RegularExpression) -> RegularExpression:
    """
        Make RegexUnion of two expressions
    """
    if isinstance(left, EmptySet):
        return right
    if isinstance(right, EmptySet):
        return left
    if left == right:
        return left
    
    return RegexUnion(left, right)


class RegexConcat(RegularExpression):
    """
        Concatenation of two expressions (L_1L_2)
    """

    def __init__(self, left: RegularExpression, right: RegularExpression):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        if isinstance(self.left, EmptyString):
            return str(self.right)
        if isinstance(self.right, EmptyString):
            return str(self.left)
        if isinstance(self.left, EmptySet) or isinstance(self.right, EmptySet):
            return "\u2205" # Unicode for ∅
        
        left_str = _add_parantheses(str(self.left))
        right_str = _add_parantheses(str(self.right))

        return f"{left_str}{right_str}"


def make_concat(left: RegularExpression, right: RegularExpression) -> RegularExpression:
    """
        Make Concatenation of two expressions
    """
    if isinstance(left, EmptyString):
        return right
    if isinstance(right, EmptyString):
        return left
    if isinstance(left, EmptySet) or isinstance(right, EmptySet):
        return EmptySet()
    return RegexConcat(left, right)


class RegexKleeneStar(RegularExpression):
    """
        Kleene Star of an expresions (L_1*)
    """

    def __init__(self, expr: RegularExpression):
        self.expr = expr

    def __str__(self) -> str:
        if isinstance(self.expr, EmptyString) or isinstance(self.expr, EmptySet):
            return "\u03b5"  # ε* = ∅* = ε 
        
        if isinstance(self.expr, RegexUnion):
            left = self.expr.left
            right = self.expr.right
            if isinstance(left, EmptyString):
                return f"{RegexKleeneStar(right)}"
            elif isinstance(right, EmptyString):
                return f"{RegexKleeneStar(left)}"
            
        expr_str = _add_parantheses(str(self.expr))

        return f"{expr_str}*"


def make_kleene_star(regex: RegularExpression) -> RegularExpression:
    """
        Make Kleene Star of an expression
    """
    if isinstance(regex, (EmptyString, EmptySet)):
        return EmptyString()
    return RegexKleeneStar(regex)


def _strip_parantheses(expr_str: str) -> str:
    """
        Remove opening and closing parantheses
    """
    if expr_str.startswith('(') and expr_str.endswith(')') and '|' in expr_str:
        return expr_str[1:-1]
    return expr_str


def _add_parantheses(expr_str: str) -> str:
    """
        Add paranthese around an union or concat expresion
    """
    if isinstance(expr_str, (RegexUnion, RegexConcat)):
        expr_str = f"({expr_str})"
    return expr_str
