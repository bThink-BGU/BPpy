from bppy import *


@b_thread
def add_hot():  # requests "HOT" three times
    yield {request: BEvent("HOT")}
    yield {request: BEvent("HOT")}
    yield {request: BEvent("HOT")}


@b_thread
def add_cold():  # requests "COLD" three times
    yield {request: BEvent("COLD")}
    yield {request: BEvent("COLD")}
    yield {request: BEvent("COLD")}


@b_thread
def control_temp():
    # This b-thread controls the temperature by blocking the previously selected event
    # and waiting for all other events in each iteration of its loop
    e = BEvent("Dummy")
    while True:
        e = yield {waitFor: All(), block: e}


if __name__ == "__main__":
    # Create a BProgram with the defined b-threads, SimpleEventSelectionStrategy,
    # and a listener to print selected events
    b_program = BProgram(bthreads=[add_hot(), add_cold(), control_temp()],
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()   # Execute the b-program
