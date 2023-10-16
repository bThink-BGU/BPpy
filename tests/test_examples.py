import unittest
import bppy as bp
from bppy.utils.z3helper import *


class TestExamples(unittest.TestCase):

    def test_hello_world(self):
        @bp.thread
        def hello():  # requests "Hello" once
            yield bp.sync(request=bp.BEvent("Hello"))

        @bp.thread
        def world():  # requests "World" once
            yield bp.sync(request=bp.BEvent("World"))

        b_program = bp.BProgram(bthreads=[hello(), world()],
                                event_selection_strategy=bp.SimpleEventSelectionStrategy())
        b_program.run()
        assert True

    def test_hot_cold_all(self):
        @bp.thread
        def add_hot():  # requests "HOT" three times
            yield bp.sync(request=bp.BEvent("HOT"))
            yield bp.sync(request=bp.BEvent("HOT"))
            yield bp.sync(request=bp.BEvent("HOT"))

        @bp.thread
        def add_cold():  # requests "COLD" three times
            yield bp.sync(request=bp.BEvent("COLD"))
            yield bp.sync(request=bp.BEvent("COLD"))
            yield bp.sync(request=bp.BEvent("COLD"))

        @bp.thread
        def control_temp():
            # This b-thread controls the temperature by blocking the previously selected event
            # and waiting for all other events in each iteration of its loop
            e = bp.BEvent("Dummy")
            while True:
                e = yield bp.sync(waitFor=bp.All(), block=e)

        b_program = bp.BProgram(bthreads=[add_hot(), add_cold(), control_temp()],
                                event_selection_strategy=bp.SimpleEventSelectionStrategy())
        b_program.run()
        assert True

    def test_hot_cold_bath(self):
        @bp.thread
        def add_hot():  # requests "HOT" three times
            yield bp.sync(request=bp.BEvent("HOT"))
            yield bp.sync(request=bp.BEvent("HOT"))
            yield bp.sync(request=bp.BEvent("HOT"))

        @bp.thread
        def add_cold():  # requests "COLD" three times
            yield bp.sync(request=bp.BEvent("COLD"))
            yield bp.sync(request=bp.BEvent("COLD"))
            yield bp.sync(request=bp.BEvent("COLD"))

        @bp.thread
        def control_temp():
            while True:
                yield bp.sync(waitFor=bp.BEvent("COLD"), block=bp.BEvent("HOT"))
                yield bp.sync(waitFor=bp.BEvent("HOT"), block=bp.BEvent("COLD"))

        b_program = bp.BProgram(bthreads=[add_hot(), add_cold(), control_temp()],
                                event_selection_strategy=bp.SimpleEventSelectionStrategy())
        b_program.run()
        assert True

    def test_hot_cold_dynamic(self):
        @bp.thread
        def add_hot():  # requests "HOT" three times
            yield bp.sync(request=bp.BEvent("HOT"))
            yield bp.sync(request=bp.BEvent("HOT"))
            yield bp.sync(request=bp.BEvent("HOT"))

        @bp.thread
        def add_cold():  # requests "COLD" three times
            yield bp.sync(request=bp.BEvent("COLD"))
            yield bp.sync(request=bp.BEvent("COLD"))
            yield bp.sync(request=bp.BEvent("COLD"))

        @bp.thread
        def control_temp(block_event):
            # This b-thread blocks the event given as an argument and then adds
            # a new b-thread with the previously selected event
            block_event = yield bp.sync(block=block_event, waitFor=bp.All())
            b_program.add_bthread(control_temp(block_event))

        b_program = bp.BProgram(bthreads=[add_hot(), add_cold(), control_temp(bp.BEvent("HOT"))],
                                event_selection_strategy=bp.SimpleEventSelectionStrategy())
        b_program.run()
        assert True

    def test_hot_cold_smt(self):
        # Defining SMT variables
        hot = Bool('hot')
        cold = Bool('cold')
        temp = Real('temp')

        @bp.thread
        def three_hot():  # requesting that the hot variable will be true three times
            for i in range(3):
                yield bp.sync(request=hot)

        @bp.thread
        def three_cold():  # requesting that the cold variable will be true three times
            for j in range(3):
                yield bp.sync(request=cold)

        @bp.thread
        def control_temp():  # blocking consecutive assignments where hot is true
            while True:
                yield bp.sync(waitFor=hot)
                yield bp.sync(block=hot, waitFor=Not(hot))

        @bp.thread
        def mutual_exclusion():  # A b-thread that ensures that cold and hot cannot be both true at the same time
            yield bp.sync(block=And(cold, hot), waitFor=false)

        @bp.thread
        def hot_temp():  # A b-thread that ensures that temp is above 50 when hot is true
            yield bp.sync(block=And(hot, temp <= 50), waitFor=false)

        @bp.thread
        def cold_temp():  # A b-thread that ensures that temp is below 50 when cold is true
            yield bp.sync(block=And(cold, temp >= 50), waitFor=false)

        @bp.thread
        def after_hot_temp():  # A b-thread that ensures that temp is above 20 when the previous event was hot
            while True:
                yield bp.sync(waitFor=hot)
                yield bp.sync(block=temp <= 20, waitFor=Not(hot))

        @bp.thread
        def after_cold_temp():  # A b-thread that ensures that temp is below 80 when the previous event was cold
            while True:
                yield bp.sync(waitFor=cold)
                yield bp.sync(block=temp >= 80, waitFor=Not(cold))

        b_program = bp.BProgram(bthreads=[three_cold(),
                                          three_hot(),
                                          mutual_exclusion(),
                                          control_temp(),
                                          hot_temp(),
                                          cold_temp(),
                                          after_hot_temp(),
                                          after_cold_temp()],
                                event_selection_strategy=bp.SMTEventSelectionStrategy())
        b_program.run()
        assert True

    def test_external_events(self):
        class External(bp.BEvent):
            pass

        any_external = bp.EventSet(lambda event: isinstance(event, External))

        @bp.thread
        def add_external():
            b_program.enqueue_external_event(External("A"))
            b_program.enqueue_external_event(External("B"))
            b_program.enqueue_external_event(External("C"))
            while True:
                yield bp.sync(waitFor=bp.All())

        @bp.thread
        def act_on_external():
            while True:
                # triggers external events if exists, else terminates the bprogram
                event = yield bp.sync(block=bp.All(), waitFor=any_external)
                yield bp.sync(request=bp.BEvent(event.name))

        b_program = bp.BProgram(bthreads=[add_external(), act_on_external()],
                                event_selection_strategy=bp.SimpleEventSelectionStrategy())
        b_program.run()
        assert True

    def test_tic_tac_toe_priorities(self):
        # BEvents functions for x and o moves
        x = lambda row, col: bp.BEvent('X' + str(row) + str(col))
        o = lambda row, col: bp.BEvent('O' + str(row) + str(col))

        # locations of all possible lines
        LINES = [[(i, j) for j in range(3)] for i in range(3)] + [[(i, j) for i in range(3)] for j in range(3)] + [
            [(i, i) for i in range(3)]] + [[(i, 3 - i - 1) for i in range(3)]]
        x_lines = [[x(i, j) for (i, j) in line] for line in LINES]
        o_lines = [[o(i, j) for (i, j) in line] for line in LINES]

        # define events sets of x an o moves
        any_x = [x(i, j) for i in range(3) for j in range(3)]
        any_o = [o(i, j) for i in range(3) for j in range(3)]
        move_events = bp.EventSet(lambda e: e.name.startswith('X') or e.name.startswith('O'))

        # define static terminal events
        static_event = {
            'OWin': bp.BEvent('OWin'),
            'XWin': bp.BEvent('XWin'),
            'draw': bp.BEvent('Draw')
        }

        @bp.thread
        def square_taken(row, col):  # blocks moves to a square that is already taken
            yield bp.sync(waitFor=[x(row, col), o(row, col)])
            yield bp.sync(block=[x(row, col), o(row, col)])

        @bp.thread
        def enforce_turns():  # blocks moves that are not in turn
            while True:
                yield bp.sync(waitFor=any_x, block=any_o)
                yield bp.sync(waitFor=any_o, block=any_x)

        @bp.thread
        def end_of_game():  # blocks moves after the game is over
            yield bp.sync(waitFor=list(static_event.values()))
            yield bp.sync(block=bp.All())

        @bp.thread
        def detect_draw():  # detects a draw
            for r in range(3):
                for c in range(3):
                    yield bp.sync(waitFor=move_events)
            yield bp.sync(request=static_event['draw'], priority=90)

        @bp.thread
        def detect_x_win(line):  # detects a win by player X
            for i in range(3):
                yield bp.sync(waitFor=line)
            yield bp.sync(request=static_event['XWin'], priority=100)

        @bp.thread
        def detect_o_win(line):  # detects a win by player O
            for i in range(3):
                yield bp.sync(waitFor=line)
            yield bp.sync(request=static_event['OWin'], priority=100)

        @bp.thread
        def center_preference():
            while True:
                yield bp.sync(request=o(1, 1), priority=35)

        @bp.thread
        def corner_preference():
            while True:
                yield bp.sync(request=[o(0, 0), o(0, 2), o(2, 0), o(2, 2)], priority=20)

        @bp.thread
        def side_preference():
            while True:
                yield bp.sync(request=[o(0, 1), o(1, 0), o(1, 2), o(2, 1)], priority=10)

        @bp.thread
        def add_third_o(line):
            for i in range(2):
                yield bp.sync(waitFor=line)
            yield bp.sync(request=line, priority=50)

        @bp.thread
        def prevent_third_x(xline, oline):
            for i in range(2):
                yield bp.sync(waitFor=xline)
            yield bp.sync(request=oline, priority=40)

        @bp.thread
        def block_fork(xfork, ofork):  # blocks a fork strategy
            for i in range(2):
                yield bp.sync(waitFor=xfork)
            yield bp.sync(request=ofork, priority=30)

        forks22 = [[x(1, 2), x(2, 0)], [x(2, 1), x(0, 2)], [x(1, 2), x(2, 1)]], [o(2, 2), o(0, 2), o(2, 0)]
        forks02 = [[x(1, 2), x(0, 0)], [x(0, 1), x(2, 2)], [x(1, 2), x(0, 1)]], [o(0, 2), o(0, 0), o(2, 2)]
        forks20 = [[x(1, 0), x(2, 2)], [x(2, 1), x(0, 0)], [x(2, 1), x(1, 0)]], [o(2, 0), o(0, 0), o(2, 2)]
        forks00 = [[x(0, 1), x(2, 0)], [x(1, 0), x(0, 2)], [x(0, 1), x(1, 0)]], [o(0, 0), o(0, 2), o(2, 0)]
        forks_diag = [[x(0, 2), x(2, 0)], [x(0, 0), x(2, 2)]], [o(0, 1), o(1, 0), o(1, 2), o(2, 1)]

        @bp.thread
        def player_x():  # simulate player X
            while True:
                yield bp.sync(request=any_x)

        bprog = bp.BProgram(
            bthreads=[square_taken(i, j) for i in range(3) for j in range(3)] +
                     [enforce_turns(), end_of_game(), detect_draw()] +
                     [detect_x_win(line) for line in x_lines] +
                     [detect_o_win(line) for line in o_lines] +
                     [center_preference(), corner_preference(), side_preference()] +
                     [add_third_o(line) for line in o_lines] +
                     [prevent_third_x(xline, oline) for (xline, oline) in zip(x_lines, o_lines)] +
                     [block_fork(xfork, forks22[1]) for xfork in forks22[0]] +
                     [block_fork(xfork, forks02[1]) for xfork in forks02[0]] +
                     [block_fork(xfork, forks20[1]) for xfork in forks20[0]] +
                     [block_fork(xfork, forks00[1]) for xfork in forks00[0]] +
                     [block_fork(xfork, forks_diag[1]) for xfork in forks_diag[0]] +
                     [player_x()],
            event_selection_strategy=bp.PriorityBasedEventSelectionStrategy(default_priority=0))
        bprog.run()
        assert True
