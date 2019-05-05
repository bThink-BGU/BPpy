from model.event_selection.event_selection_strategy import EventSelectionStrategy
from z3 import *


class SMTEventSelectionStrategy(EventSelectionStrategy):

    def is_satisfied(self, event, statement):
        return is_true(event.eval(statement.get('wait-for', self.true)))  # TODO: not sure if it's the right approach

    def __init__(self):
        self.true = BoolSort().cast(True)
        self.false = BoolSort().cast(False)

    def select(self, statements):
        (request, block) = (self.false, self.false)

        # Collect request and block statements
        for l in statements:
            request = Or(request, l.get('request', self.false))
            block = Or(block, l.get('block', self.false))

        # Compute a satisfying assignment
        sl = Solver()
        sl.add(And(request, Not(block)))
        if sl.check() == sat:
            return sl.model()
        else:
            return None


