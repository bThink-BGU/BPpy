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
    while True:
        yield bp.sync(waitFor=bp.BEvent("COLD"), block=bp.BEvent("HOT"))
        yield bp.sync(waitFor=bp.BEvent("HOT"), block=bp.BEvent("COLD"))


if __name__ == "__main__":
    b_program = bp.BProgram(bthreads=[add_hot(), add_cold(), control_temp()],
                            event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                            listener=bp.PrintBProgramRunnerListener())
    b_program.run()
