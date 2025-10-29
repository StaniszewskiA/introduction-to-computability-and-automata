from src.regular.regular_expression import EmptySet, EmptyString, RegularExpression, Symbol, make_concat, make_kleene_star, make_union

class RegexConvertible:
    """
        Mixin for regex conversion.
    """
    def to_regex(self) -> RegularExpression:
        states = self.get_states()
        R: dict[str, dict[str, RegularExpression]] = {}
        for state1 in states:
            R[state1] = {}
            for state2 in states:
                R[state1][state2] = EmptySet()
        for from_state, transitions in self.delta.items():
            for symbol, target in transitions.items():
                if symbol == '':
                    symbol_regex = EmptyString()
                else:
                    symbol_regex = Symbol(symbol)
                if hasattr(self, 'step') and callable(getattr(self, 'step', None)) and not isinstance(target, set):
                    to_state = target
                    curr_symbol = R[from_state][to_state]
                    if isinstance(curr_symbol, EmptySet):
                        R[from_state][to_state] = symbol_regex
                    else:
                        R[from_state][to_state] = make_union(curr_symbol, symbol_regex)
                else:
                    for to_state in target:
                        curr_symbol = R[from_state][to_state]
                        if isinstance(curr_symbol, EmptySet):
                            R[from_state][to_state] = symbol_regex
                        else:
                            R[from_state][to_state] = make_union(curr_symbol, symbol_regex)
        if len(self.final_states) > 1:
            new_final_state = "F_new"
            states.add(new_final_state)
            R[new_final_state] = {}
            for state in states:
                if state != new_final_state:
                    R[state][new_final_state] = EmptySet()
                R[new_final_state][state] = EmptySet()
            for final_state in self.final_states:
                R[final_state][new_final_state] = EmptyString()
            final_state = new_final_state
        else:
            final_state = next(iter(self.final_states))
        elimination_order = [state for state in states if state not in (self.start, final_state)]
        for k in elimination_order:
            remaining_states = [state for state in states if state != k]
            for i in remaining_states:
                for j in remaining_states:
                    old_path = R[i][j]
                    new_path = make_concat(
                        make_concat(R[i][k], make_kleene_star(R[k][k])),
                        R[k][j]
                    )
                    R[i][j] = make_union(old_path, new_path)
            states.remove(k)
        start_loop = R[self.start][self.start]
        direct_path = R[self.start][final_state]
        if isinstance(start_loop, EmptySet):
            return direct_path
        return make_concat(make_kleene_star(start_loop), direct_path)
