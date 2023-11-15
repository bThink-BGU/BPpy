import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import thread
from bppy.analysis.bprogram_converter import BProgramConverter
import itertools

'''
Monty Hall problem:
Show host hides a prize behind one of three doors. A player guesses a door.
The host opens one of the other doors, revealing no prize.
The player can now choose to stick with their original choice or switch to the other door.
'''

@thread
def game_show(): # b-thread for the game show host
	yield sync(request=bp.BEvent('why'))
	# choice may be made before the bthread starts
	hide = yield choice({1: 0.33, 2: 0.33, 3: 0.33}) # the value returned is equivalent to sampling the distribution
	yield sync(request=bp.BEvent(f'h{hide}'))
	guess_string = yield choice({'g1': 0.33, 'g2': 0.33, 'g3': 0.33}) # the domain can be any value that can be used in a dict
	yield sync(request= bp.BEvent(guess_string))
	opened = yield sync(request=[bp.BEvent(f'o{i}') for i in range(1, 4)]) # only one of these will be the selected event
	final_choice = yield sync(request= [bp.BEvent(f'c{i}') for i in range(1, 4)])

@thread
def block_opening_prize(): # prevent the host from opening the door with the prize
	hideEvent = yield sync(waitFor=[bp.BEvent(f'h{i}') for i in range(1, 4)])
	hideDoor = hideEvent.name[1:]
	yield sync(block= bp.BEvent(f'o{hideDoor}'))

@thread
def block_opening_guess(): # prevent the host from opening the door the player guessed
	guessEvent = yield sync(waitFor=[bp.BEvent(f'g{i}') for i in range(1, 4)])
	guessDoor = guessEvent.name[1:]
	yield sync(block=bp.BEvent(f'o{guessDoor}'))

@thread
def block_choosing_opened_doors(): # whenever a door is opened, block it from being chosen at the end
	choiceEvent = yield sync(waitFor=[bp.BEvent(f'o{i}') for i in range(1, 4)])
	choiceDoor = choiceEvent.name[1:]
	yield sync(block=bp.BEvent(f'c{choiceDoor}'))


if __name__ == '__main__':
	def bp_gen():
		return bp.BProgram(bthreads=[game_show(), block_opening_prize(), block_opening_guess(), block_choosing_opened_doors()],
						event_selection_strategy=bp.SimpleEventSelectionStrategy())
	events = [bp.BEvent(f'{action}{i}') for action, i in itertools.product(['h', 'g', 'o', 'c'], range(1, 4))]
	converter = BProgramConverter(bp_gen, events, ["game", "prize", "guess", "doors_opened"])
	content = converter.to_prism()
	#converter.to_prism('examples/monty_out.pm')
	