import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import b_thread
from bppy.analysis.bprogram_converter import BProgramConverter
import itertools


@b_thread
def host():
	hide = yield Choice({1: 0.33, 2: 0.33, 3: 0.33})
	yield BSync({request: bp.BEvent(f'h{hide}')})
	guess = yield Choice({1: 0.33, 2: 0.33, 3: 0.33})
	yield BSync({request: bp.BEvent(f'g{guess}')})
	opened = yield BSync({request: [bp.BEvent(f"o{i}") for i in range(1, 4)]})

@b_thread
def car():
	hideEvent = yield BSync({waitFor: [bp.BEvent(f"h{i}") for i in range(1, 4)]})
	hideDoor = hideEvent.name[1:]
	yield BSync({block: bp.BEvent(f'o{hideDoor}')})

@b_thread
def guess():
	guessEvent = yield BSync({waitFor: [bp.BEvent(f"g{i}") for i in range(1, 4)]})
	guessDoor = guessEvent.name[1:]
	yield BSync({block: bp.BEvent(f'o{guessDoor}')})

if __name__ == "__main__":
	def bp_gen():
		return bp.BProgram(bthreads=[host(), car(), guess()],
						event_selection_strategy=bp.SimpleEventSelectionStrategy())
	events = [bp.BEvent(f'{action}{i}') for action, i in itertools.product(['h', 'g', 'o'], range(1, 4))]
	converter = BProgramConverter(bp_gen, events, ["host", "car", "guest"])
	converter.to_prism('examples/monty_out.pm')
	