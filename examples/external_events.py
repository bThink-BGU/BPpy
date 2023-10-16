import bppy as bp


# define an external event class
class External(bp.BEvent):
    pass


# define an internal event class
class Internal(bp.BEvent):
    pass


# define idle event class
class Idle(bp.BEvent):
    def __init__(self):
        super().__init__("IDLE")


# define the set of external and internal events
any_external = bp.EventSet(lambda event: isinstance(event, External))
any_internal = bp.EventSet(lambda event: isinstance(event, Internal))


@bp.thread
def worker():
    # waits for external job event and then operates on it
    while True:
        event = yield bp.sync(waitFor=any_external)
        # do something with the external job event
        yield bp.sync(request=Internal("Done processing job " + event.name))


@bp.thread
def manager():
    # waits for internal events and then declares that the system is idle
    while True:
        yield bp.sync(request=Idle())
        yield bp.sync(waitFor=any_internal)


# define a listener that submits jobs to the bprogram when idle
class JobsListener(bp.PrintBProgramRunnerListener):
    def __init__(self):
        super().__init__()
        self.jobs = ["A", "B", "C"]

    def event_selected(self, b_program, event):
        super().event_selected(b_program, event)
        if isinstance(event, Idle):
            if self.jobs:
                b_program.enqueue_external_event(External("Submitted job " + self.jobs.pop(0)))


if __name__ == "__main__":
    b_program = bp.BProgram(bthreads=[worker(), manager()],
                            event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                            listener=JobsListener())
    b_program.run()
