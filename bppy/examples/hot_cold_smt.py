from bppy import *

hot = Bool('hot')
cold = Bool('cold')


@b_thread
def three_hot():
    for i in range(3):
        while (yield {request: hot})[hot] == false:
            pass


@b_thread
def three_cold():
    for j in range(3):
        m = yield {request: cold}
        while m[cold] == false:
            m = yield {request: cold}


@b_thread
def exclusion():
    while True:
        yield {block: And(hot, cold)}


@b_thread
def schedule():
    yield {block: cold}


if __name__ == "__main__":
    b_program = BProgram(bthreads=[three_cold(), three_hot(), exclusion(), schedule()],
                         event_selection_strategy=SMTEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()
