import bppy as bp


@bp.thread
def add_hot():  # requests "HOT" three times
    yield bp.sync(request=bp.BEvent("HOT"))
    yield bp.sync(request=bp.BEvent("HOT"))
    yield bp.sync(request=bp.BEvent("HOT"))


@bp.thread
def add_cold():  # requests "COLD" three times
    yield bp.sync(request=bp.BEvent("COLD"))
    yield bp.sync(request=bp.BEvent("COLD"))
    yield bp.sync(request=bp.BEvent("COLD"))


@bp.thread
def control_temp():
    # This b-thread controls the temperature by blocking the previously selected event
    # and waiting for all other events in each iteration of its loop
    e = bp.BEvent("Dummy")
    while True:
        e = yield bp.sync(waitFor=bp.All(), block=e)


if __name__ == "__main__":
    # Create a BProgram with the defined b-threads, SimpleEventSelectionStrategy,
    # and a listener to print selected events
    b_program = bp.BProgram(bthreads=[add_hot(), add_cold(), control_temp()],
                            event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                            listener=bp.PrintBProgramRunnerListener())
    b_program.run()  # Execute the b-program
