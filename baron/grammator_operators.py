from utils import assignment


def include_operators(pg):
    @pg.production("old_test : or_test")
    @pg.production("old_test : old_lambdef")
    def old_test((level,)):
        return level


    @pg.production("testlist_safe : old_test comma old_test")
    def testlist_safe((old_test, comma, old_test2)):
        return [old_test, comma, old_test2]


    @pg.production("testlist_safe : old_test comma testlist_safe")
    def testlist_safe_more((old_test, comma, testlist_safe)):
        return [old_test, comma] + testlist_safe


    @pg.production("expr_stmt : testlist PLUS_EQUAL testlist")
    @pg.production("expr_stmt : testlist MINUS_EQUAL testlist")
    @pg.production("expr_stmt : testlist STAR_EQUAL testlist")
    @pg.production("expr_stmt : testlist SLASH_EQUAL testlist")
    @pg.production("expr_stmt : testlist PERCENT_EQUAL testlist")
    @pg.production("expr_stmt : testlist AMPER_EQUAL testlist")
    @pg.production("expr_stmt : testlist VBAR_EQUAL testlist")
    @pg.production("expr_stmt : testlist CIRCUMFLEX_EQUAL testlist")
    @pg.production("expr_stmt : testlist LEFT_SHIFT_EQUAL testlist")
    @pg.production("expr_stmt : testlist RIGHT_SHIFT_EQUAL testlist")
    @pg.production("expr_stmt : testlist DOUBLE_STAR_EQUAL testlist")
    @pg.production("expr_stmt : testlist DOUBLE_SLASH_EQUAL testlist")
    def augmented_assignment_node((target, operator, value)):
        return {
            "type": "assign",
            "first_space": operator.before_space,
            "second_space": operator.after_space,
            "operator": operator.value[:-1],
            "target": target,
            "value": value
        }


    @pg.production("expr_stmt : testlist EQUAL expr_stmt")
    def assignment_node((target, equal, value)):
        return assignment(value, target, equal.before_space, equal.after_space)


    @pg.production("test : or_test IF or_test ELSE test")
    def ternary_operator_node((first, if_, second, else_, third)):
        return {
            "type": "ternary_operator",
            "first": first,
            "second": third,
            "value": second,
            "first_space": if_.before_space,
            "second_space": if_.after_space,
            "third_space": else_.before_space,
            "forth_space": else_.after_space,
        }


    @pg.production("or_test : and_test OR or_test")
    @pg.production("and_test : not_test AND and_test")
    def and_or_node((first, operator, second)):
        return {
            "type": "boolean_operator",
            "value": operator.value,
            "first": first,
            "second": second,
            "first_space": operator.before_space,
            "second_space": operator.after_space,
        }


    @pg.production("not_test : NOT not_test")
    def not_node((not_, comparison)):
        return {
            "type": "unitary_operator",
            "value": "not",
            "target": comparison,
            "space": not_.after_space
        }


    @pg.production("comparison : expr LESS comparison")
    @pg.production("comparison : expr GREATER comparison")
    @pg.production("comparison : expr EQUAL_EQUAL comparison")
    @pg.production("comparison : expr LESS_EQUAL comparison")
    @pg.production("comparison : expr GREATER_EQUAL comparison")
    @pg.production("comparison : expr LESS_GREATER comparison")
    @pg.production("comparison : expr NOT_EQUAL comparison")
    @pg.production("comparison : expr IN comparison")
    @pg.production("comparison : expr IS comparison")
    def comparison_node((expr, comparison_operator, comparison_)):
        return {
            "type": "comparison",
            "value": comparison_operator.value,
            "middle_space": "",
            "first": expr,
            "second": comparison_,
            "first_space": comparison_operator.before_space,
            "second_space": comparison_operator.after_space
        }


    @pg.production("comparison : expr IS NOT comparison")
    @pg.production("comparison : expr NOT IN comparison")
    def comparison_advanced_node((expr, comparison_operator, comparison_operator2, comparison_)):
        return {
            "type": "comparison",
            "value": "%s %s" % (
                comparison_operator.value,
                comparison_operator2.value
            ),
            "first": expr,
            "second": comparison_,
            "first_space": comparison_operator.before_space,
            "second_space": comparison_operator2.after_space,
            "middle_space": comparison_operator.after_space,
        }


    @pg.production("expr : xor_expr VBAR expr")
    @pg.production("xor_expr : and_expr CIRCUMFLEX xor_expr")
    @pg.production("and_expr : shift_expr AMPER and_expr")
    @pg.production("shift_expr : arith_expr RIGHT_SHIFT shift_expr")
    @pg.production("shift_expr : arith_expr LEFT_SHIFT shift_expr")
    @pg.production("arith_expr : term PLUS arith_expr")
    @pg.production("arith_expr : term MINUS arith_expr")
    @pg.production("term : factor STAR term")
    @pg.production("term : factor SLASH term")
    @pg.production("term : factor PERCENT term")
    @pg.production("term : factor DOUBLE_SLASH term")
    @pg.production("power : atom DOUBLE_STAR factor")
    @pg.production("power : atom DOUBLE_STAR power")
    def binary_operator_node((first, operator, second)):
        return {
            "type": "binary_operator",
            "value": operator.value,
            "first": first,
            "second": second,
            "first_space": operator.before_space,
            "second_space": operator.after_space
        }


    @pg.production("factor : PLUS factor")
    @pg.production("factor : MINUS factor")
    @pg.production("factor : TILDE factor")
    def factor_unitary_operator_space((operator, factor,)):
        return {
            "type": "unitary_operator",
            "value": operator.value,
            "space": operator.after_space,
            "target": factor,
        }


    @pg.production("power : atomtrailers DOUBLE_STAR factor")
    @pg.production("power : atomtrailers DOUBLE_STAR power")
    def power_atomtrailer_power((atomtrailers, double_star, factor)):
        return {
            "type": "binary_operator",
            "value": double_star.value,
            "first": {
                "type": "atomtrailers",
                "value": atomtrailers,
            },
            "second": factor,
            "first_space": double_star.before_space,
            "second_space": double_star.after_space
        }


    @pg.production("power : atomtrailers")
    def power_atomtrailers((atomtrailers,)):
        return {
            "type": "atomtrailers",
            "value": atomtrailers
        }


    @pg.production("atomtrailers : atom")
    def atomtrailers_atom((atom,)):
        return [atom]


    @pg.production("atomtrailers : atom trailers")
    def atomtrailer((atom, trailers)):
        return [atom] + trailers


    @pg.production("trailers : trailer")
    def trailers((trailer,)):
        return trailer


    @pg.production("trailers : trailers trailer")
    def trailers_trailer((trailers, trailer)):
        return trailers + trailer


    @pg.production("trailer : DOT NAME")
    def trailer((dot, name,)):
        return [{
            "type": "dot",
            "first_space": dot.before_space,
            "second_space": dot.after_space,
        },{
            "type": "name",
            "value": name.value,
        }]


    @pg.production("trailer : LEFT_PARENTHESIS argslist RIGHT_PARENTHESIS")
    def trailer_call((left, argslist, right)):
        return [{
            "type": "call",
            "value": [],
            "first_space": left.before_space,
            "second_space": left.after_space,
            "third_space": right.before_space,
        }]


    @pg.production("trailer : LEFT_SQUARE_BRACKET subscript RIGHT_SQUARE_BRACKET")
    @pg.production("trailer : LEFT_SQUARE_BRACKET subscriptlist RIGHT_SQUARE_BRACKET")
    def trailer_getitem_ellipsis((left, subscript, right)):
        return [{
            "type": "getitem" if left.value == "[" else "call",
            "value": subscript,
            "first_space": left.after_space,
            "second_space": right.before_space,
        }]


    @pg.production("subscript : DOT DOT DOT")
    def subscript_ellipsis((dot1, dot2, dot3)):
        return {
            "type": "ellipsis",
            "first_space": dot1.after_space,
            "second_space": dot2.after_space,
        }


    @pg.production("subscript : test")
    @pg.production("subscript : slice")
    def subscript_test((test,)):
        return test

    @pg.production("slice : COLON COLON?")
    def slice((colon, colon2)):
        return {
            "type": "slice",
            "lower": None,
            "upper": None,
            "step": None,
            "has_two_colons": bool(colon2),
            "first_space": "",
            "second_space": colon.after_space,
            "third_space": "",
            "forth_space": "",
        }

    @pg.production("slice : test COLON COLON?")
    def slice_lower((test, colon, colon2)):
        return {
            "type": "slice",
            "lower": test,
            "upper": None,
            "step": None,
            "has_two_colons": bool(colon2),
            "first_space": colon.before_space,
            "second_space": colon.after_space,
            "third_space": "",
            "forth_space": "",
        }

    @pg.production("slice : COLON test COLON?")
    def slice_upper((colon, test, colon2)):
        return {
            "type": "slice",
            "lower": None,
            "upper": test,
            "step": None,
            "has_two_colons": bool(colon2),
            "first_space": colon.before_space,
            "second_space": colon.after_space,
            "third_space": colon2.before_space if colon2 else "",
            "forth_space": "",
        }

    @pg.production("slice : COLON COLON test")
    def slice_step((colon, colon2, test)):
        return {
            "type": "slice",
            "lower": None,
            "upper": None,
            "step": test,
            "has_two_colons": True,
            "first_space": colon.before_space,
            "second_space": colon.after_space,
            "third_space": colon2.before_space,
            "forth_space": colon2.after_space,
        }

    @pg.production("slice : test COLON test COLON?")
    def slice_lower_upper((test, colon, test2, colon2)):
        return {
            "type": "slice",
            "lower": test,
            "upper": test2,
            "step": None,
            "has_two_colons": bool(colon2),
            "first_space": colon.before_space,
            "second_space": colon.after_space,
            "third_space": colon2.before_space if colon2 else "",
            "forth_space": "",
        }

    @pg.production("slice : test COLON COLON test")
    def slice_lower_step((test, colon, colon2, test2)):
        return {
            "type": "slice",
            "lower": test,
            "upper": None,
            "step": test2,
            "has_two_colons": True,
            "first_space": colon.before_space,
            "second_space": colon.after_space,
            "third_space": colon2.before_space,
            "forth_space": colon2.after_space,
        }

    @pg.production("slice : COLON test COLON test")
    def slice_upper_step((colon, test, colon2, test2)):
        return {
            "type": "slice",
            "lower": None,
            "upper": test,
            "step": test2,
            "has_two_colons": True,
            "first_space": colon.before_space,
            "second_space": colon.after_space,
            "third_space": colon2.before_space,
            "forth_space": colon2.after_space,
        }

    @pg.production("slice : test COLON test COLON test")
    def slice_lower_upper_step((test, colon2, test2, colon, test3)):
        return {
            "type": "slice",
            "lower": test,
            "upper": test2,
            "step": test3,
            "has_two_colons": True,
            "first_space": colon.before_space,
            "second_space": colon.after_space,
            "third_space": colon2.before_space,
            "forth_space": colon2.after_space,
        }
