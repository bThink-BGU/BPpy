import bppy as bp
from bppy import BEvent
from bppy.model.sync_statement import *
from bppy.model.b_thread import b_thread
from bppy.analysis.bprogram_to_prism import prism_converter
from bppy.utils.probability import Choice


@b_thread
def host():
	r = yield Choice({'a': 0.2, 'b': 0.3, 'c': 0.5})
	yield BSync({request: BEvent(f'event_{r}')})


if __name__ == "__main__":
	def bp_gen():
		return bp.BProgram(bthreads=[host()],
						event_selection_strategy=bp.SimpleEventSelectionStrategy(),
						listener=bp.PrintBProgramRunnerListener())
	prism = prism_converter(bp_gen,
				[BEvent(f"event_{chr(ord('a')+i)}") for i in range(0, 3)],
				["host"])