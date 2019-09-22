from model.b_event import BEvent
from execution.listeners.print_b_program_runner_listener import PrintBProgramRunnerListener
from model.bprogram import BProgram
from model.event_selection.simple_event_selection_strategy import SimpleEventSelectionStrategy



def add_hot():
    yield {'request': BEvent(name="HOT")}
    yield {'request': BEvent(name="HOT")}
    yield {'request': BEvent(name="HOT")}


def add_cold():
    yield {'request': BEvent(name="COLD")}
    yield {'request': BEvent(name="COLD")}
    yield {'request': BEvent(name="COLD")}


def control_temp():
    while True:
        yield {'waitFor': BEvent(name="COLD"), 'block': BEvent(name="HOT")}
        yield {'waitFor': BEvent(name="HOT"), 'block': BEvent(name="COLD")}


if __name__ == "__main__":
    b_program = BProgram(source_name="hot_cold_bath",
                         #bthreads=[add_hot(), add_cold(), control_temp()],
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()
