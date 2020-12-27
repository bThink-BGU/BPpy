from bppy import *

hot = Bool('hot')
cold = Bool('cold')

@b_thread
def three_hot():
    for i in range(3):
        yield {request: hot , waitFor: hot}

@b_thread
def three_cold():
    for j in range(3):
        yield {request: cold , waitFor: cold}

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
    yield {block: And(cold ,hot), waitFor: false}


if __name__ == "__main__":
    b_program = BProgram(bthreads=[three_cold(), three_hot(), mutual_exclusion(), control_temp()],
                         event_selection_strategy=SMTEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()
