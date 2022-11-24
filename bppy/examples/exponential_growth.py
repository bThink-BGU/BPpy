from bppy import *


@b_thread
def exponential_growth(exp):
    yield {request: BEvent(f"{exp}")}
    if exp > 0:
        b_program.add_bthread(exponential_growth(exp - 1))
        b_program.add_bthread(exponential_growth(exp - 1))


if __name__ == "__main__":
    b_program = BProgram(bthreads=[exponential_growth(4)],
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()
