from bppy import *

hot = Bool('hot')
cold = Bool('cold')


def three_hot():
    for i in range(3):
        while (yield {request: hot})[hot] == false:
            pass


def three_cold():
    for j in range(3):
        m = yield {request: cold}
        while m[cold] == false:
            m = yield {request: cold}


def exclusion():
    while True:
        yield {block: And(hot, cold)}


def schedule():
    yield {block: cold}


if __name__ == "__main__":
    b_program = BProgram(bthreads=[three_cold(), three_hot(), exclusion(), schedule()],
                         event_selection_strategy=SMTEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()
