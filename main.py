from execution.listeners.print_b_program_runner_listener import PrintBProgramRunnerListener
from model.bprogram import BProgram
from model.event_selection.smt_event_selection_strategy import SMTEventSelectionStrategy

if __name__ == "__main__":
    # b_program = Bprogram(source_name="hot_cold_bath",
    #                      event_selection_strategy=SimpleEventSelectionStrategy(),
    #                      listener=PrintBProgramRunnerListener())
    b_program = BProgram(source_name="hot_cold_smt",
                         event_selection_strategy=SMTEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()
