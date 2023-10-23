from bppy.model.b_event import BEvent
from bppy.model.event_set import EventSet
from bppy.model.sync_statement import BSync
from bppy.utils.dfs import DFSBProgram
from bppy.utils.exceptions import BPAssertionError
from collections.abc import Iterable
from probabilities import Choice


# adjusting https://github.com/bThink-BGU/BPpy/blob/master/bppy/utils/dfs.py
# program to only map individual threads without the graph exploration


def prism_converter(bprogram_generator, event_list, bt_names):

	dfs = DFSBProgram(bprogram_generator, event_list)
	init, mapper = dfs.run(explore_graph=False)

	event_names = [x.name for x in dfs.event_list]
	events = {e: BEvent(e) for e in event_names}
	bp_states = {bt_names[i]:v for i, v in mapper.items()}

	rule_template = "formula is_{}_{} = {};"
	bt_condition = "(is_{}_{}_{}={})"

	header = 'mdp\n\n'

	req = [rule_template.format(e, "requested",
			' | '.join([bt_condition.format(bt,'requesting',e,'true')
			for bt in bt_names]))
		for e in event_names]

	block = [rule_template.format(e, "blocked",
			' | '.join([bt_condition.format(bt,'blocking',e,'true')
			for bt in bt_names]))
		for e in event_names]

	select = [rule_template.format(e, "selected",
			' & '.join([f'(is_{e}_requested=true)',
						f'(is_{e}_blocked=false)']))
		for e in event_names]

	labels = ["label \"{}\" = (is_{}_selected=true);".format(e, e)
		for e in event_names]

	header += '\n\n'.join(
		['\n'.join(sec) for sec in [req,block,select,labels]])

	header += '\n//-----------------------\n\n'

	def format_bt_module(name, event_names, bt_states):

		node_to_s = {s: i for i, s in enumerate(bp_states[name])}

		bt_req = {e: [] for e in event_names}
		bt_block = {e: [] for e in event_names}
		bt_trans = {}
		bt_probs = {}

		for node, n in node_to_s.items():
			if isinstance(node.data, BSync):
				bt_trans[n] = {}
				for e in event_names:
					if ('request' in node.data):
						if (isinstance(node.data['request'], Iterable) and
								events[e] in node.data['request']):
							bt_req[e].append(n)
						elif (isinstance(node.data['request'], BEvent) and
								events[e] == node.data['request']):
							bt_req[e].append(n)
					if ('block' in node.data):
						if (isinstance(node.data['block'], Iterable) and
								events[e] in node.data['block']):
							bt_block[e].append(n)
						elif (isinstance(node.data['block'], BEvent) and
								events[e] == node.data['block']):
							bt_block[e].append(n)
					bt_trans[n][e] = (node_to_s[node.transitions[events[e]]] if
									events[e] in node.transitions else n)
			if isinstance(node.data, Choice):
				bt_probs[n] = {rand_choice: (node_to_s[node.transitions[rand_choice][0]],
											 node.transitions[rand_choice][1])
									for rand_choice in node.data.keys()}

		module_template = '\nmodule {}\n\t{}\n\n\t{}\nendmodule\n'
		state_template = "formula is_{}_{}_{} = {};"
		state_name = f's_{name}'
		state_init = f'{state_name}: [0..{len(bt_states)-1}] init 0;'
		event_transition = '[{}] ({}={}) & (is_{}_selected=true) -> 1: ({}\'={});'
		prob_transition = '[] ({}={}) -> {};'
		prob_format = '{}: ({}\'={})'

		req = [state_template.format(name, "requesting", e,
				' | '.join([('({}={})').format(state_name, n)
				for n in bt_req[e]]) if len(bt_req[e]) > 0 else 'false')
			for e in event_names]

		block = [state_template.format(name, "blocking", e,
				' | '.join([('({}={})').format(state_name, n)
				for n in bt_block[e]]) if len(bt_block[e]) > 0 else 'false')
			for e in event_names]

		transitions = []
		for n, tr in bt_trans.items():
			string_tr = [event_transition.format(e, state_name,
							n, e, state_name, s_tag) for e, s_tag in tr.items()]
			transitions.append('\n\t'.join(string_tr))
		
		probabilities = []
		for n, choice in bt_probs.items():
			string_prob = [prob_format.format(p, state_name, next_state)
							for next_state, p in choice.values()]
			probabilities.append(prob_transition.format(state_name, n,
								' + '.join(string_prob)))

		module = ''
		module += '\n\n'.join(
			['\n'.join(sec) for sec in [req,block]])

		module += module_template.format(name,
								state_init, '\n\t\n\t'.join(transitions + probabilities))

		return module


	content = '\n\n'.join([format_bt_module(bt_name, event_names,
							bp_states[bt_name]) for bt_name in bt_names])
	
	return header + content

