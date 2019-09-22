from model.b_event import BEvent
from execution.listeners.print_b_program_runner_listener import PrintBProgramRunnerListener
from model.bprogram import BProgram
from model.event_selection.simple_event_selection_strategy import SimpleEventSelectionStrategy


def hello():
    yield {'request': BEvent(name="Hello")}


def world():
    yield {'request': BEvent(name="World")}


if __name__ == "__main__":
    b_program = BProgram(bthreads=[hello(), world()],
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()
