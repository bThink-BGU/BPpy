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
def control_temp(block_event):
    # This b-thread blocks the event given as an argument and then adds
    # a new b-thread with the previously selected event
    block_event = yield {waitFor: All(), block: block_event}
    b_program.add_bthread(control_temp(block_event))


if __name__ == "__main__":
    b_program = BProgram(bthreads=[add_hot(), add_cold(), control_temp(BEvent("HOT"))],
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()