from bppy import *

class External(BEvent):
    pass


any_external = EventSet(lambda event: isinstance(event, External))

@b_thread
def add_external():
    b_program.enqueue_external_event(External("A"))
    b_program.enqueue_external_event(External("B"))
    b_program.enqueue_external_event(External("C"))
    while True:
        yield {waitFor: All()}

@b_thread
def act_on_external():
    while True:
        # triggers external events if exists, else terminates the bprogram
        event = yield {block: All(), waitFor: any_external}
        yield {request: BEvent(event.name)}


if __name__ == "__main__":
    b_program = BProgram(bthreads=[add_external(), act_on_external()],
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()
