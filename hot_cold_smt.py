from z3 import Int, is_true, And, BoolSort, Bool

hot = Bool('hot')
cold = Bool('cold')


def three_hot():
    for i in range(3):
        while (yield {'request': hot})[hot] == BoolSort().cast(False):
            pass


def three_cold():
    for j in range(3):
        m = yield {'request': cold}
        while m[cold] == BoolSort().cast(False):
            m = yield {'request': cold}


def no_two_same_in_a_row():
    m = yield {}
    while True:
        if m[cold] == BoolSort().cast(True):
            m = yield {'block': cold}
        if is_true(m[hot]):
            m = yield {'block': hot}


def exclusion():
    while True:
        yield {'block': And(hot, cold)}


def schedule():
    yield {'block': cold}