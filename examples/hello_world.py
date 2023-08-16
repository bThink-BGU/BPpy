from bppy import *


@b_thread
def hello():  # requests "Hello" once
    yield {request: BEvent("Hello")}

@b_thread
def world():  # requests "World" once
    yield {request: BEvent("World")}


if __name__ == "__main__":
    # Create a BProgram with two b-threads (hello and world), a simple event selection strategy, and a listener that
    # prints the selected events
    b_program = BProgram(bthreads=[hello(), world()],
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    # Run the BProgram
    b_program.run()
