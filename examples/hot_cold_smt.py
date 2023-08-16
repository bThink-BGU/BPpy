from bppy import *

hot = Bool('hot')
cold = Bool('cold')
temp = Real('temp')


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
        yield {waitFor: hot}
        yield {block: hot, waitFor: cold}


@b_thread
def mutual_exclusion():
    yield {block: And(cold, hot), waitFor: false}


@b_thread
def hot_temp():
    while True:
        yield {block: And(hot, temp <= 50), waitFor: false}


@b_thread
def cold_temp():
    while True:
        yield {block: And(cold, temp >= 50), waitFor: false}


@b_thread
def after_hot_temp():
    while True:
        m = yield {waitFor: hot}
        while is_true(m[hot]):
            m = yield {block: temp <= 20}


@b_thread
def after_cold_temp():
    while True:
        m = yield {waitFor: cold}
        while is_true(m[cold]):
            m = yield {block: temp >= 80}


if __name__ == "__main__":
    b_program = BProgram(bthreads=[three_cold(),
                                   three_hot(),
                                   mutual_exclusion(),
                                   control_temp(),
                                   hot_temp(),
                                   cold_temp(),
                                   after_hot_temp(),
                                   after_cold_temp()],
                         event_selection_strategy=SMTEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()
