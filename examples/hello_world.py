import bppy as bp


@bp.thread
def hello():  # requests "Hello" once
    yield bp.sync(request=bp.BEvent("Hello"))


@bp.thread
def world():  # requests "World" once
    yield bp.sync(request=bp.BEvent("World"))


if __name__ == "__main__":
    # Create a BProgram with two b-threads (hello and world), a simple event selection strategy, and a listener that
    # prints the selected events
    b_program = bp.BProgram(bthreads=[hello(), world()],
                            event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                            listener=bp.PrintBProgramRunnerListener())
    # Run the BProgram
    b_program.run()
