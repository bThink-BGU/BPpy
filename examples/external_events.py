from bppy import *

# define an external event class
class External(BEvent):
    pass

# define the set of external events
any_external = EventSet(lambda event: isinstance(event, External))

@b_thread
def add_external():  # adds external events to the bprogram and then continues doing nothing
    b_program.enqueue_external_event(External("A"))
    b_program.enqueue_external_event(External("B"))
    b_program.enqueue_external_event(External("C"))
    while True:
        yield {waitFor: All()}

@b_thread
def act_on_external():
    # waits for external events, while blocking all internal events
    # and then requests an internal event with the same name
    while True:
        # triggers external events if exists, else terminates the bprogram
        event = yield {block: All(), waitFor: any_external}
        yield {request: BEvent(event.name)}


if __name__ == "__main__":
    b_program = BProgram(bthreads=[add_external(), act_on_external()],
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()
