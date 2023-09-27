from bppy import *


# define an external event class
class External(BEvent):
    pass


# define an internal event class
class Internal(BEvent):
    pass


# define idle event class
class Idle(BEvent):
    def __init__(self):
        super().__init__("IDLE")


# define the set of external and internal events
any_external = EventSet(lambda event: isinstance(event, External))
any_internal = EventSet(lambda event: isinstance(event, Internal))


@b_thread
def worker():
    # waits for external job event and then operates on it
    while True:
        event = yield {waitFor: any_external}
        # do something with the external job event
        yield {request: Internal("Done processing job " + event.name)}


@b_thread
def manager():
    # waits for internal events and then declares that the system is idle
    while True:
        yield {request: Idle()}
        yield {waitFor: any_internal}


# define a listener that submits jobs to the bprogram when idle
class JobsListener(PrintBProgramRunnerListener):
    def __init__(self):
        super().__init__()
        self.jobs = ["A", "B", "C"]

    def event_selected(self, b_program, event):
        super().event_selected(b_program, event)
        if isinstance(event, Idle):
            if self.jobs:
                b_program.enqueue_external_event(External("Submitted job " + self.jobs.pop(0)))


if __name__ == "__main__":
    b_program = BProgram(bthreads=[worker(), manager()],
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=JobsListener())
    b_program.run()
