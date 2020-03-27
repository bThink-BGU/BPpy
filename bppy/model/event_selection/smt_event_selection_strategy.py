from bppy.model.event_selection.event_selection_strategy import EventSelectionStrategy
from bppy.utils.z3helper import *


class SMTEventSelectionStrategy(EventSelectionStrategy):

    def is_satisfied(self, event, statement):
        return is_true(event.eval(statement.get('wait-for', true)))  # TODO: not sure if it's the right approach

    def select(self, statements, additional_statement=None):
        (request, block) = (false, false)

        # Collect request and block statements
        for l in statements:
            request = Or(request, l.get('request', false))
            block = Or(block, l.get('block', false))

        if additional_statement:
            request = Or(request, additional_statement.get('request', false))
            block = Or(block, additional_statement.get('block', false))


        # Compute a satisfying assignment
        sl = Solver()
        sl.add(And(request, Not(block)))
        if sl.check() == sat:
            return sl.model()
        else:
            return None


