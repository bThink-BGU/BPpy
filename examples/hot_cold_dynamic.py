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
def control_temp(block_event):
    # This b-thread blocks the event given as an argument and then adds
    # a new b-thread with the previously selected event
    block_event = yield bp.sync(block=block_event, waitFor=bp.All())
    b_program.add_bthread(control_temp(block_event))


if __name__ == "__main__":
    b_program = bp.BProgram(bthreads=[add_hot(), add_cold(), control_temp(bp.BEvent("HOT"))],
                            event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                            listener=bp.PrintBProgramRunnerListener())
    b_program.run()
