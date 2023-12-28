import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import *
from bppy.analysis.bprogram_converter import BProgramConverter
import itertools


@analysis_thread
def game_show(): # b-thread for the game show host
	# choice may be made before the bthread starts
	hide = yield choice({1: 0.34, 2: 0.33, 3: 0.33}) # the value returned is equivalent to sampling the distribution
	yield sync(request=bp.BEvent(f'h{hide}'))
	guess = yield sync(waitFor=[bp.BEvent(f'g{i}') for i in range(1, 4)]) # wait for the player to make a guess
	doors_possible = [door for door in [1, 2, 3] if door not in [hide, int(guess.name[1:])]]
	opened = yield choice({door: 1/len(doors_possible) for door in doors_possible})
	yield sync(request=bp.BEvent('o'+str(opened))) # only one of these will be selected

@analysis_thread
def contestant():
	yield sync(waitFor=[bp.BEvent(f'h{i}') for i in range(1, 4)]) # wait for the host to hide the prize
	guess = yield choice({'g1': 0.34, 'g2': 0.33, 'g3': 0.33}) # the domain can be any value that can be used in a dict
	yield sync(request=bp.BEvent(guess))
	o = yield sync(waitFor=[bp.BEvent(f'o{i}') for i in range(1, 4)])
	final_choice = yield sync(request=[bp.BEvent(f'c{i}') for i in range(1, 4)])

@analysis_thread
def block_choosing_opened_doors(): # prevent the player from picking an opened door
	choiceEvent = yield sync(waitFor=[bp.BEvent(f'o{i}') for i in range(1, 4)])
	choiceDoor = choiceEvent.name[1:]
	yield sync(block=bp.BEvent(f'c{choiceDoor}'))

if __name__ == '__main__':
	def bp_gen():
		return bp.BProgram(bthreads=[game_show(), contestant(), block_choosing_opened_doors()],
						event_selection_strategy=bp.SimpleEventSelectionStrategy(),
						listener=bp.PrintBProgramRunnerListener())
	events = [bp.BEvent(f'{action}{i}') for action, i in itertools.product(['h', 'g', 'o', 'c'], range(1, 4))]
	converter = BProgramConverter(bp_gen, events, ["host", "contestant","block_door"])
	content = converter.to_prism()
	#converter.to_prism('monty_out.pm')
	