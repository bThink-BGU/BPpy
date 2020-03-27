import sys
import os
from bppy.model.event_selection.event_selection_strategy import EventSelectionStrategy
from bppy.utils.z3helper import *


class Request:
    def __init__(self, variables=None):
        self.variables = variables


class WaitFor:
    pass


class Block:
    pass


class ExperimentalSMTEventSelectionStrategy(EventSelectionStrategy):

    def __init__(self, debug=False):
        self.debug = debug

    def is_satisfied(self, event, statement):
        return is_true(event.eval(statement.get(WaitFor, true)))

    def select(self, statements):
        sl = Solver()

        # Collect the blocking constraints
        blocking = Not(Or([l.get(Block, false) for l in statements]))
        sl.add(blocking)

        # A dictionary that maps each variable to a disjunction of all the requests for the variable
        requests = {}

        # Make sure that the model assigns a value to each of the variables that appear in any of the statements
        for l in statements:
            for v in getVariables(l.get(Block, false)):
                requests[v] = false

            for v in getVariables(l.get(Request, false)):
                requests[v] = false

        # Fill the requests dictionary
        for l in statements:
            for key, req in l.items():
                if isinstance(key, Request) or key == Request:
                    if key == Request or key.variables is None:
                        vars = getVariables(req)
                    else:
                        vars = key.variables

                    for v in vars:
                        requests[v] = Or(requests.get(v, false), req)

        # Add each of the disjunctionin requests to the solver
        for r in requests.values():
            sl.add(r)

        # Use this to debug the assertions
        if self.debug:
            print(">> Block=", simplify(blocking))
            print(">> Requests=")
            for key, value in requests.items():
                print(">>\t {} -> {}".format(key,simplify(value)))

        if sl.check() == sat:
            return sl.model()
        else:
            return None
