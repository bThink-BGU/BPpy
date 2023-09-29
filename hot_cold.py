import bppy as bp
from bppy import BEvent
from bppy.model.sync_statement import *
from bppy.model.b_thread import b_thread
from bppy_to_prism import prism_converter

@b_thread
def add_hot():  # requests "HOT" three times
    yield {request: BEvent("HOT")}
    yield {request: BEvent("HOT")}


@b_thread
def add_cold():  # requests "COLD" three times
    yield {request: BEvent("COLD")}
    yield {request: BEvent("COLD")}

@b_thread
def add_random():
	which_var = yield Dist.Categorical({'X': 0.5, 'Y': 0.5})

@b_thread
def control():
    while True:
        yield {waitFor: BEvent("COLD"), block: [BEvent("HOT"), BEvent("Y")]}
        yield {waitFor: BEvent("HOT"), block: BEvent("COLD")}

# function that generates a b-program with the control b-thread

if __name__ == "__main__":

	def bp_gen():
		return bp.BProgram(bthreads=[add_hot(), add_cold(), add_random(), control()],
						event_selection_strategy=bp.ProbabilisticEventSelectionStrategy(),
						listener=bp.PrintBProgramRunnerListener())
	prog = bp_gen()
	prog.run()

	prism = prism_converter(bp_gen,
				[bp.BEvent("HOT"), bp.BEvent("COLD"), bp.BEvent("X"), bp.BEvent("Y")],
				["bt_hot", "bt_cold", "add_random", "interweave"])
	
	with open("BProgram.pm", "w") as f:
		f.write(prism)