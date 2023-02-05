from bppy.model.event_selection.solver_based_event_selection_strategy import SolverBasedEventSelectionStrategy
from bppy.utils.z3helper import *


class SMTEventSelectionStrategy(SolverBasedEventSelectionStrategy):

    def is_satisfied(self, event, statement):
        return is_true(event.eval(statement.get('waitFor', true)))  

    # TODO: implement a way to set additional_statement
    def select(self, statements, additional_statement=None):
        if isinstance(additional_statement, list) and len(additional_statement) > 0:
            raise NotImplementedError("SMTEventSelectionStrategy does not support external events.")
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


