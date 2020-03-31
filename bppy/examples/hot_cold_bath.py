from bppy import *


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


if __name__ == "__main__":
    b_program = BProgram(bthreads=[add_hot(), add_cold(), control_temp()],
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()
