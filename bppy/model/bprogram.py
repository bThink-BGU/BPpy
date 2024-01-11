from importlib import import_module
from inspect import getmembers, isfunction
from itertools import tee
import warnings

from z3 import *


class BProgram:
    """
    A class to represent a Behavioral Program (BProgram) object.

    Attributes
    ----------
    source_name : str
        A file name from which bthreads are imported.
    new_bt : list
        A list of new bthreads that have not been loaded yet.
    bthreads : list
        A list of bthreads to be run in the BProgram.
    event_selection_strategy : :class:`EventSelectionStrategy <bppy.model.event_selection.event_selection_strategy.EventSelectionStrategy>`
        A strategy object to select events and advance bthreads.
    listener : :class:`BProgramRunnerListener <bppy.execution.listeners.b_program_runner_listener.BProgramRunnerListener>`
        A listener object to be invoked at the start and end of the program, and at each event selection.
    variables : dict
        A dictionary of variables declared in the source module (for SMT based event selection startegy).
    tickets : list
        A list of bthread tickets (used in execution).
    external_events_queue : list
        A queue to handle external events introduced into the BProgram.
    """
    def __init__(self, bthreads=None, source_name=None, event_selection_strategy=None, listener=None):
        """
        Constructs all the necessary attributes for the BProgram object.

        Parameters
        ----------
        bthreads : list, optional
            A list of bthreads to be run in the BProgram.
        source_name : str, optional
            The module from which bthreads are imported. If this is provided,
            the bthreads and variables from the source module will be imported when setup() is called.
        event_selection_strategy : :class:`EventSelectionStrategy <bppy.model.event_selection.event_selection_strategy.EventSelectionStrategy>`, optional
            An event selection strategy object.
        listener : :class:`BProgramRunnerListener <bppy.execution.listeners.b_program_runner_listener.BProgramRunnerListener>`, optional
            A bprogram listener object.
        """
        self.source_name = source_name
        self.new_bt = []
        self.bthreads = bthreads
        self.event_selection_strategy = event_selection_strategy
        self.listener = listener
        self.variables = None
        self.tickets = []
        self.external_events_queue = []

    def setup(self):
        """
        Sets up the BProgram.

        If a source file is provided, this method imports all bthreads and variables
        into the BProgram. All bthreads are then loaded.
        """
        if self.source_name:
            self.bthreads = [o[1]() for o in getmembers(import_module(self.source_name)) if
                             isfunction(o[1]) and o[1].__module__ == self.source_name]

            self.variables = dict([o for o in getmembers(import_module(self.source_name)) if
                                   isinstance(o[1], ExprRef) or isinstance(o[1], list)])

        self.new_bt = self.bthreads
        self.load_new_bthreads()


    def advance_bthreads(self,tickets, m):
        """
        Advances bthreads based on the selected event (m), using the event selection strategy satisfactions criteria (e.g., event was requested or waited for).

        Parameters
        ----------
        tickets : list
            A list of bthread tickets.
        m : :class:`BEvent <bppy.model.b_event.BEvent>`
            The selected event to be sent as message to the bthreads.
        """
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
        """
        Adds a new bthread to the BProgram (should be loaded after using :func:`load_new_bthreads <bppy.model.bprogram.BProgram.load_new_bthreads>`).

        Parameters
        ----------
        bt : Any
            The bthread to be added.
        """
        self.new_bt.append(bt)

    def load_new_bthreads(self):
        """
        Loads all new bthreads into the BProgram.

        The method uses :func:`advance_bthreads <bppy.model.bprogram.BProgram.advance_bthreads>` to load bthreads.
        """
        while len(self.new_bt) > 0:
            new_tickets = [{'bt': bt} for bt in self.new_bt]
            for bt in self.new_bt:
                if bt.gi_frame.f_locals['mode'] == 'analysis':
                    warnings.warn("Some new bthreads are analysis bthreads and will not affect the bprogram execution correctly.", RuntimeWarning)
            self.new_bt.clear()
            self.advance_bthreads(new_tickets, None)
            self.tickets.extend(new_tickets)

    def next_event(self):
        """
        Selects the next event in the BProgram using the event selection strategy.

        If there are new bthreads that haven't been loaded, a warning will be raised.

        Returns
        -------
        event : :class:`BEvent <bppy.model.b_event.BEvent>`
            The selected event to be processed.
        """
        if len(self.new_bt) > 0:
            warnings.warn(
                "Some new bthreads are not loaded and are not affecting the bprogram. Use the load_new_bthreads method to load them.",
                RuntimeWarning)
        return self.event_selection_strategy.select(self.tickets, self.external_events_queue)

    def run(self):
        """
        Runs the BProgram.

        It sets up the BProgram, selects events, and advance the bthreads until no event can be selected
        or until interrupted by the listener. At the start and end of the run, and after each
        event selection, the listener (if provided) is invoked.
        """
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
        """
        Enqueues an external event into the BProgram.

        Parameters
        ----------
        event : :class:`BEvent <bppy.model.b_event.BEvent>`
            The external event to be enqueued.
        """
        self.external_events_queue.append(event)
