from z3 import *

true = BoolSort().cast(True)
false = BoolSort().cast(False)


def toFloat(r):
    return float(r.numerator_as_long()) / float(r.denominator_as_long())


def visitor(e, seen):
    if e in seen:
        return
    seen[e] = True
    yield e
    if is_app(e):
        for ch in e.children():
            for e in visitor(ch, seen):
                yield e
        return
    if is_quantifier(e):
        for e in visitor(e.body(), seen):
            yield e
        return


def printVars(fml):
    seen = {}
    for e in visitor(fml, seen):
        if is_const(e) and e.decl().kind() == Z3_OP_UNINTERPRETED:
            print("Variable", e)
        else:
            print(e)


def getVariables(fml):
    seen = {}
    for e in visitor(fml, seen):
        if is_const(e) and e.decl().kind() == Z3_OP_UNINTERPRETED:
            yield e
