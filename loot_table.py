import bppy as bp
from bppy.utils.dfs import DFSBProgram
from bppy.analysis.bprogram_converter import BProgramConverter


'''
Modeling https://oldschool.runescape.wiki/w/Chest_(Tombs_of_Amascut)
'''

purple_rewards = {'staff': (1/10, 150), 'ring': (1/2, 50), 'sword': (0.4, 150)} # (rate, level)
white_rewards = {'coins': 1, 'sapphire': 200, 'diamond': 400, 'helmet': 4000} # divisior value

@bp.thread
def team_unique_roll(total_points, level):
	x = min(level, 400)
	y = max(level - 400, 0)
	pts_for_percent = 10500 - 20 * (x + y / 3.)
	purple_chance = max( 0.01 * total_points / pts_for_percent, 0.55)
	result = yield bp.choice({'raid_purple': purple_chance, 'raid_white': 1 - purple_chance})
	yield bp.sync(request=bp.BEvent(result))


@bp.thread
def distribute_unique_drop(total_points, personal_points_arr):
	yield bp.sync(waitFor=bp.BEvent('raid_purple'))
	num_players = len(personal_points_arr)
	recipient = yield bp.choice({i: personal_points_arr[i] / total_points for i in range(num_players)})
	for i in range(num_players):
		if i == recipient:
			yield bp.sync(request=bp.BEvent(f'p{i}_purple'))
		else:
			yield bp.sync(request=bp.BEvent(f'p{i}_white'))

@bp.thread
def distribute_normal_drop(total_points, personal_points_arr):
	yield bp.sync(waitFor=bp.BEvent('raid_white'))
	num_players = len(personal_points_arr)
	for i in range(num_players):
		yield bp.sync(request=bp.BEvent(f'p{i}_normal'))

@bp.thread
def roll_unique_drop(level):
	recipient_event = yield bp.sync(waitFor=bp.BEvent([f'p{i}_purple' for i in range(len(personal_points_arr))]))
	recipient = p.name[1]
	item = yield bp.choice({item: rate for item, (rate, _) in purple_rewards.items()})
	

@bp.thread
def ignore_level_restriction(level):
	yield bp.sync(waitFor=bp.BEvent(f'raid_purple'))
	restriction = yield bp.choice({'ignore': 1/50, 'dont_ignore': 49/50})
	if ignore_restriction == 'dont_ignore':
		blocked_events = [item for item, (_, item_level) in purple_rewards.items() if item_level > level]
		yield bp.sync(block=bp.BEvent(f'{player}_loot_{item}'))
	if purple_rewards[item.name[5:]][1] > level:
		

def bp_gen():
	return bp.BProgram(bthreads=[main()],
					event_selection_strategy=bp.SimpleEventSelectionStrategy())

converter = BProgramConverter(bp_gen, [bp.BEvent('a'), bp.BEvent('b'), bp.BEvent('c')])
# converter.to_prism(None)