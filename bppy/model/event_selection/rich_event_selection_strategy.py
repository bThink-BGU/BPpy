from bppy.model.event_selection.smt_event_selection_strategy import SMTEventSelectionStrategy
from bppy.utils.z3helper import *


class RichEventSelectionStrategy(SMTEventSelectionStrategy):
    """
    A solver-based implementation of EventSelectionStrategy using z3 SMT solver. The strategy used is the one
    presented in the paper `Executing Scenario-Based Specification with Dynamic Generation of Rich Events
    <https://www.wisdom.weizmann.ac.il/~dharel/papers/CCIS2019RichEvents.pdf>`_.
    """

    def is_satisfied(self, event, statement):
        return is_true(event.eval(statement.get('waitFor', true), model_completion=True))

