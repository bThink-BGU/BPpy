from bppy import *

# Defining SMT variables
hot = Bool('hot')
cold = Bool('cold')
temp = Real('temp')


@b_thread
def three_hot():  # requesting that the hot variable will be true three times
    for i in range(3):
        yield {request: hot}


@b_thread
def three_cold():  # requesting that the cold variable will be true three times
    for j in range(3):
        yield {request: cold}


@b_thread
def control_temp():  # blocking consecutive assignments where hot is true
    while True:
        yield {waitFor: hot}
        yield {block: hot, waitFor: cold}


@b_thread
def mutual_exclusion():  # A b-thread that ensures that cold and hot cannot be both true at the same time
    yield {block: And(cold, hot), waitFor: false}


@b_thread
def hot_temp():  # A b-thread that ensures that temp is above 50 when hot is true
    yield {block: And(hot, temp <= 50), waitFor: false}


@b_thread
def cold_temp():  # A b-thread that ensures that temp is below 50 when cold is true
    yield {block: And(cold, temp >= 50), waitFor: false}


@b_thread
def after_hot_temp():  # A b-thread that ensures that temp is above 20 when the previous event was hot
    while True:
        yield {waitFor: hot}
        yield {block: temp <= 20, waitFor: Not(hot)}


@b_thread
def after_cold_temp():  # A b-thread that ensures that temp is below 80 when the previous event was cold
    while True:
        yield {waitFor: cold}
        yield {block: temp >= 80, waitFor: Not(cold)}


if __name__ == "__main__":
    # Creating a BProgram with the defined b-threads, SMTEventSelectionStrategy,
    # and a listener to print the selected events
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
