from importlib import import_module
from inspect import getmembers, isfunction
from itertools import tee
import warnings

from z3 import *


class BProgram:

    def __init__(self, bthreads=None, source_name=None, event_selection_strategy=None, listener=None):
        self.source_name = source_name
        self.new_bt = []
        self.bthreads = bthreads
        self.event_selection_strategy = event_selection_strategy
        self.listener = listener
        self.variables = None
        self.tickets = []
        self.external_events_queue = []

    def setup(self):
        if self.source_name:
            self.bthreads = [o[1]() for o in getmembers(import_module(self.source_name)) if
                             isfunction(o[1]) and o[1].__module__ == self.source_name]

            self.variables = dict([o for o in getmembers(import_module(self.source_name)) if
                                   isinstance(o[1], ExprRef) or isinstance(o[1], list)])

        self.new_bt = self.bthreads
        self.load_new_bthreads()


    def advance_bthreads(self,tickets, m):
        if len(self.new_bt) > 0:
            warnings.warn("Some new bthreads are not loaded and are not affecting the bprogram. Use the load_new_bthreads method to load them.", RuntimeWarning)
        for l in tickets:
            if m is None or self.event_selection_strategy.is_satisfied(m, l):
                try:
                    bt = l['bt']
                    l.clear()
                    ll = bt.send(m)
                    if ll is None:
                        continue
                    l.update(ll)
                    l.update({'bt': bt})
                except (KeyError, StopIteration):
                    pass

    def add_bthread(self, bt):
        self.new_bt.append(bt)

    def load_new_bthreads(self):
        while len(self.new_bt) > 0:
            new_tickets = [{'bt': bt} for bt in self.new_bt]
            self.new_bt.clear()
            self.advance_bthreads(new_tickets, None)
            self.tickets.extend(new_tickets)

    def next_event(self):
        if len(self.new_bt) > 0:
            warnings.warn(
                "Some new bthreads are not loaded and are not affecting the bprogram. Use the load_new_bthreads method to load them.",
                RuntimeWarning)
        return self.event_selection_strategy.select(self.tickets, self.external_events_queue)

    def run(self):
        if self.listener:
            self.listener.starting(b_program=self)

        self.setup()
        # Main loop
        interrupted = False
        while not interrupted:
            # for dynamically added bthreads
            self.load_new_bthreads()

            event = self.next_event()
            # Finish the program if no event is selected
            if event is None:
                break
            if self.listener:
                interrupted = self.listener.event_selected(b_program=self, event=event)

            self.advance_bthreads(self.tickets,event)


        if self.listener:
            self.listener.ended(b_program=self)

    def enqueue_external_event(self, event):
        self.external_events_queue.append(event)
