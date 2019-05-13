from model.event_selection.event_selection_strategy import EventSelectionStrategy
from z3helper import *


class ExperimentalSMTEventSelectionStrategy(EventSelectionStrategy):

    def is_satisfied(self, event, statement):
        return is_true(event.eval(statement.get('wait-for', true)))

    def select(self, statements):
        sl = Optimize()

        sl.add(Not(Or([l.get('block', false) for l in statements])))

        requests = {}

        for l in statements:
            req = l.get('request')
            if req is not None:
                for v in getVariables(req):
                    requests[v] = Or(requests.get(v, false), req)

        for r in requests.values():
            sl.add(r)

        sl.maximize(Real('p'))

        if sl.check() == sat:
            return sl.model()
        else:
            return None
