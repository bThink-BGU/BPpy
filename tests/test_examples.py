import unittest
from bppy import *


class TestExamples(unittest.TestCase):

    def test_hello_world(self):
        @b_thread
        def hello():
            yield {request: BEvent("Hello")}

        @b_thread
        def world():
            yield {request: BEvent("World")}
        b_program = BProgram(bthreads=[hello(), world()],
                             event_selection_strategy=SimpleEventSelectionStrategy())
        b_program.run()
        assert True

    def test_hot_cold_all(self):
        @b_thread
        def add_hot():
            yield {request: BEvent("HOT")}
            yield {request: BEvent("HOT")}
            yield {request: BEvent("HOT")}

        @b_thread
        def add_cold():
            yield {request: BEvent("COLD")}
            yield {request: BEvent("COLD")}
            yield {request: BEvent("COLD")}

        @b_thread
        def control_temp():
            e = BEvent("Dummy")
            while True:
                e = yield {waitFor: All(), block: e}

        b_program = BProgram(bthreads=[add_hot(), add_cold(), control_temp()],
                             event_selection_strategy=SimpleEventSelectionStrategy())
        b_program.run()
        assert True

    def test_hot_cold_bath(self):
        @b_thread
        def add_hot():
            yield {request: BEvent("HOT")}
            yield {request: BEvent("HOT")}
            yield {request: BEvent("HOT")}

        @b_thread
        def add_cold():
            yield {request: BEvent("COLD")}
            yield {request: BEvent("COLD")}
            yield {request: BEvent("COLD")}

        @b_thread
        def control_temp():
            while True:
                yield {waitFor: BEvent("COLD"), block: BEvent("HOT")}
                yield {waitFor: BEvent("HOT"), block: BEvent("COLD")}

        b_program = BProgram(bthreads=[add_hot(), add_cold(), control_temp()],
                             event_selection_strategy=SimpleEventSelectionStrategy())
        b_program.run()
        assert True

    def test_hot_cold_dynamic(self):
        @b_thread
        def add_hot():
            yield {request: BEvent("HOT")}
            yield {request: BEvent("HOT")}
            yield {request: BEvent("HOT")}

        @b_thread
        def add_cold():
            yield {request: BEvent("COLD")}
            yield {request: BEvent("COLD")}
            yield {request: BEvent("COLD")}

        @b_thread
        def control_temp(block_event):
            block_event = yield {waitFor: All(), block: block_event}
            b_program.add_bthread(control_temp(block_event))

        b_program = BProgram(bthreads=[add_hot(), add_cold(), control_temp(BEvent("HOT"))],
                             event_selection_strategy=SimpleEventSelectionStrategy())
        b_program.run()
        assert True

    def test_hot_cold_smt(self):
        hot = Bool('hot')
        cold = Bool('cold')

        @b_thread
        def three_hot():
            for i in range(3):
                yield {request: hot, waitFor: hot}

        @b_thread
        def three_cold():
            for j in range(3):
                yield {request: cold, waitFor: cold}

        @b_thread
        def control_temp():
            m = yield {}
            while True:
                if is_true(m[cold]):
                    m = yield {block: cold}
                if is_true(m[hot]):
                    m = yield {block: hot}

        @b_thread
        def mutual_exclusion():
            yield {block: And(cold, hot), waitFor: false}

        b_program = BProgram(bthreads=[three_cold(), three_hot(), mutual_exclusion(), control_temp()],
                             event_selection_strategy=SMTEventSelectionStrategy())
        b_program.run()
        assert True

    def test_external_events(self):
        class External(BEvent):
            pass

        any_external = EventSet(lambda event: isinstance(event, External))

        @b_thread
        def add_external():
            b_program.enqueue_external_event(External("A"))
            b_program.enqueue_external_event(External("B"))
            b_program.enqueue_external_event(External("C"))
            while True:
                yield {waitFor: All()}

        @b_thread
        def act_on_external():
            while True:
                # triggers external events if exists, else terminates the bprogram
                event = yield {block: All(), waitFor: any_external}
                yield {request: BEvent(event.name)}

        b_program = BProgram(bthreads=[add_external(), act_on_external()],
                             event_selection_strategy=SimpleEventSelectionStrategy())
        b_program.run()
        assert True

    def test_tic_tac_toe_priorities(self):
        x = lambda row, col: BEvent('X' + str(row) + str(col))
        o = lambda row, col: BEvent('O' + str(row) + str(col))

        LINES = [[(i, j) for j in range(3)] for i in range(3)] + [[(i, j) for i in range(3)] for j in range(3)] + [
            [(i, i) for i in range(3)]] + [[(i, 3 - i - 1) for i in range(3)]]
        x_lines = [[x(i, j) for (i, j) in line] for line in LINES]
        o_lines = [[o(i, j) for (i, j) in line] for line in LINES]

        any_x = [x(i, j) for i in range(3) for j in range(3)]
        any_o = [o(i, j) for i in range(3) for j in range(3)]
        move_events = EventSet(lambda e: e.name.startswith('X') or e.name.startswith('O'))

        static_event = {
            'OWin': BEvent('OWin'),
            'XWin': BEvent('XWin'),
            'draw': BEvent('Draw')
        }

        @b_thread
        def square_taken(row, col):
            yield {waitFor: [x(row, col), o(row, col)]}
            yield {block: [x(row, col), o(row, col)]}

        @b_thread
        def enforce_turns():
            while True:
                yield {waitFor: any_x, block: any_o}
                yield {waitFor: any_o, block: any_x}

        @b_thread
        def end_of_game():
            yield {waitFor: list(static_event.values())}
            yield {block: All()}

        @b_thread
        def detect_draw():
            for r in range(3):
                for c in range(3):
                    yield {waitFor: move_events}
            yield {request: static_event['draw'], priority: 90}

        @b_thread
        def detect_x_win(line):
            for i in range(3):
                yield {waitFor: line}
            yield {request: static_event['XWin'], priority: 100}

        @b_thread
        def detect_o_win(line):
            for i in range(3):
                yield {waitFor: line}
            yield {request: static_event['OWin'], priority: 100}

        # Preference to put O on the center
        @b_thread
        def center_preference():
            while True:
                yield {request: o(1, 1), priority: 35}

        # Preference to put O on the corners
        @b_thread
        def corner_preference():
            while True:
                yield {request: [o(0, 0), o(0, 2), o(2, 0), o(2, 2)], priority: 20}

        # Preference to put O on the sides
        @b_thread
        def side_preference():
            while True:
                yield {request: [o(0, 1), o(1, 0), o(1, 2), o(2, 1)], priority: 10}

        # player O strategy to add a third O to win
        @b_thread
        def add_third_o(line):
            for i in range(2):
                yield {waitFor: line}
            yield {request: line, priority: 50}

        # player O strategy to prevent a third X
        @b_thread
        def prevent_third_x(xline, oline):
            for i in range(2):
                yield {waitFor: xline}
            yield {request: oline, priority: 40}

        @b_thread
        def block_fork(xfork, ofork):
            for i in range(2):
                yield {waitFor: xfork}
            yield {request: ofork, priority: 30}

        forks22 = [[x(1, 2), x(2, 0)], [x(2, 1), x(0, 2)], [x(1, 2), x(2, 1)]], [o(2, 2), o(0, 2), o(2, 0)]
        forks02 = [[x(1, 2), x(0, 0)], [x(0, 1), x(2, 2)], [x(1, 2), x(0, 1)]], [o(0, 2), o(0, 0), o(2, 2)]
        forks20 = [[x(1, 0), x(2, 2)], [x(2, 1), x(0, 0)], [x(2, 1), x(1, 0)]], [o(2, 0), o(0, 0), o(2, 2)]
        forks00 = [[x(0, 1), x(2, 0)], [x(1, 0), x(0, 2)], [x(0, 1), x(1, 0)]], [o(0, 0), o(0, 2), o(2, 0)]
        forks_diag = [[x(0, 2), x(2, 0)], [x(0, 0), x(2, 2)]], [o(0, 1), o(1, 0), o(1, 2), o(2, 1)]

        # simulate player X
        @b_thread
        def player_x():
            while True:
                yield {request: any_x}

        bprog = BProgram(
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
            event_selection_strategy=PriorityBasedEventSelectionStrategy(default_priority=0))
        bprog.run()
        assert True