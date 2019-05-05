from model.bprogram import Bprogram
from execution.listeners.print_b_program_runner_listener import PrintBProgramRunnerListener
from model.event_selection.smt_event_selection_strategy import SMTEventSelectionStrategy
from model.event_selection.simple_event_selection_strategy import SimpleEventSelectionStrategy

if __name__ == "__main__":
    source_name = "hot_cold_bath"
    b_program = Bprogram(source_name=source_name,
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    # b_program = Bprogram(source_name=source_name,
    #                      event_selection_strategy=SMTEventSelectionStrategy(),
    #                      listener=PrintBProgramRunnerListener())
    b_program.run()
