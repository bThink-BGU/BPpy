import bppy as bp
from bppy import BEvent
from bppy.model.sync_statement import *
from bppy.model.b_thread import b_thread
from bppy_to_prism import prism_converter
from distributions import Categorical



@b_thread
def host():
	hide = Categorical('hide', {'h1': 0.33, 'h2': 0.33, 'h3': 0.33})
	yield {request: BEvent(hide)}
	guess = yield Categorical('hide', {'g1': 0.33, 'g2': 0.33, 'g3': 0.33})
	yield {request: BEvent(guess)}
	# h = yield {request: [BEvent(f"h{i}") for i in range(1, 4)]}
	# g = yield {request: [BEvent(f"g{i}") for i in range(1, 4)]}
	o = yield {request: [BEvent(f"o{i}") for i in range(1, 4)]}

@b_thread
def car():
	hideEvent = yield {waitFor: [BEvent(f"h{i}") for i in range(1, 4)]}
	hideDoor = hideEvent.name[1:]
	yield {block: BEvent(f'o{hideDoor}')}

@b_thread
def guess():
	guessEvent = yield {waitFor: [BEvent(f"g{i}") for i in range(1, 4)]}
	guessDoor = guessEvent.name[1:]
	yield {block: BEvent(f'o{guessDoor}')}

if __name__ == "__main__":

	def bp_gen():
		return bp.BProgram(bthreads=[host(), car(), guess()],
						event_selection_strategy=bp.SimpleEventSelectionStrategy(),
						listener=bp.PrintBProgramRunnerListener())
	prism = prism_converter(bp_gen,
				[BEvent(f"h{i}") for i in range(1, 4)]+[BEvent(f"g{i}") for i in range(1, 4)]+[BEvent(f"o{i}") for i in range(1, 4)],
				["host", "car", "player"])
	with open("monty_out.pm", "w") as f:
		f.write(prism)