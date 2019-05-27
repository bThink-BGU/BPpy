from z3 import *

from execution.listeners.print_b_program_runner_listener import PrintBProgramRunnerListener
from model.bprogram import BProgram
from model.event_selection.smt_event_selection_strategy import SMTEventSelectionStrategy
from z3helper import *


hot = Bool('hot')
cold = Bool('cold')


def three_hot():
    for i in range(3):
        while (yield {'request': hot})[hot] == false:
            pass


def three_cold():
    for j in range(3):
        m = yield {'request': cold}
        while m[cold] == false:
            m = yield {'request': cold}


def no_two_same_in_a_row():
    m = yield {}
    while True:
        if m[cold] == true:
            m = yield {'block': cold}
        if is_true(m[hot]):
            m = yield {'block': hot}


def exclusion():
    while True:
        yield {'block': And(hot, cold)}


def schedule():
    yield {'block': cold}


if __name__ == "__main__":
    b_program = BProgram(bthreads=[three_cold(), three_hot(), exclusion(), no_two_same_in_a_row()],
                         event_selection_strategy=SMTEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()
