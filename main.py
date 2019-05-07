from execution.listeners.print_b_program_runner_listener import PrintBProgramRunnerListener
from model.bprogram import BProgram
from model.event_selection.simple_event_selection_strategy import SimpleEventSelectionStrategy

if __name__ == "__main__":
    b_program = BProgram(source_name="hot_cold_bath",
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    # b_program = BProgram(source_name="hot_cold_smt",
    #                      event_selection_strategy=SMTEventSelectionStrategy(),
    #                      listener=PrintBProgramRunnerListener())
    b_program.run()
