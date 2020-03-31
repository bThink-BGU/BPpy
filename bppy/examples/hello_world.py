from bppy import *


@b_thread
def hello():
    yield {request: BEvent("Hello")}

@b_thread
def world():
    yield {request: BEvent("World")}


if __name__ == "__main__":
    b_program = BProgram(bthreads=[hello(), world()],
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()
