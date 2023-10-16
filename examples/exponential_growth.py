import bppy as bp


@bp.thread
def exponential_growth(exp):
    yield bp.sync(request=bp.BEvent(f"{exp}"))
    if exp > 0:
        b_program.add_bthread(exponential_growth(exp - 1))
        b_program.add_bthread(exponential_growth(exp - 1))


if __name__ == "__main__":
    b_program = bp.BProgram(bthreads=[exponential_growth(4)],
                            event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                            listener=bp.PrintBProgramRunnerListener())
    b_program.run()
