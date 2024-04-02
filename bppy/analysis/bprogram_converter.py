from bppy.model.b_event import BEvent
from bppy.model.event_set import EventSet
from bppy.model.sync_statement import sync, choice
from bppy.utils.dfs import DFSBProgram
from bppy.utils.exceptions import BPAssertionError
from collections.abc import Iterable


class BProgramConverter:
	"""
	A class to convert a behavioral program to a PRISM model by exploring the DFS graph.
	"""
	def __init__(self, bprogram_generator, event_list, bt_names=None, max_trace_length=1000):
		"""
		Initialize a DFSBProgramVerifier.

		Parameters:
		-----------
		bprogram_generator : function
			A function that generates a new instance of the BProgram.
		event_list : list
			A list of event objects which are used in the model.
		bt_names : list, optional
			Names to used for the matching bthreads in the prism model.
			If none, the bthreads are named bt0, bt1, etc.
		max_trace_length : int, optional
			Maximum length of the trace before terminating the search. Defaults to 1000.
		"""
		self.bprogram_generator = bprogram_generator
		self.event_list = event_list
		if bt_names is not None:
			self.bt_names = bt_names
		else:
			names = [f'bt{i}' for i in range(len(self.bprogram_generator().bthreads))]
			self.bt_names = names
		self.max_trace_length = max_trace_length

	def collect_structure(self):
		"""
		Generates the tree structure and other necessary details of the behavioral program.
		"""
		dfs = DFSBProgram(self.bprogram_generator, self.event_list,
			max_trace_length=self.max_trace_length)
		init, mapper = dfs.run(explore_graph=False)

		names = [x.name for x in dfs.event_list]
		events = {e: BEvent(e) for e in names}
		bp_states = {self.bt_names[i]:v for i, v in mapper.items()}

		return names, events, bp_states

	#def 

	def to_prism(self, output_file=None):
		"""
		Converts the behavioral program to a PRISM model of a markov decision process, with each bthread corresponding to a module.
		Returns the resulting text content.

		Parameters
		----------
		output_file : str, optional
			Name of the file to write the PRISM model to.
			Defaults to 'None'.
		"""

		event_names, events, bp_states = self.collect_structure()

		rule_template = "formula {}_{} = {};"
		bt_condition = "({}_{}_{}={})"

		header = 'dtmc\n\n'

		def map_bt_states(event_names, bt_states):
			node_to_s = {s: i for i, s in enumerate(bt_states)}
			relevant_events = {e: False for e in event_names}

			bt_req = {e: [] for e in event_names}
			bt_block = {e: [] for e in event_names}
			bt_trans = {}
			bt_probs = {}

			for node, n in node_to_s.items():
				if isinstance(node.data, sync):
					bt_trans[n] = {}
					if ('request' in node.data):
						if isinstance(node.data['request'], Iterable):
							for e in node.data['request']:
								bt_req[e.name].append(n)
						elif isinstance(node.data['request'], BEvent):
							bt_req[node.data['request'].name].append(n)
						else:
							raise BPAssertionError("Request of an unknown type")
					if ('block' in node.data):
						if isinstance(node.data['block'], Iterable):
							for e in node.data['block']:
								bt_block[e.name].append(n)
						elif isinstance(node.data['block'], BEvent):
							bt_block[node.data['block'].name].append(n)
						else:
							raise BPAssertionError("Block of an unknown type")
					for e in event_names:
						bt_trans[n][e] = (node_to_s[node.transitions[events[e]]] if
								events[e] in node.transitions else n)
					for t in node.transitions:
						if node.transitions[t] != node: 
							relevant_events[t.name] = True
				if isinstance(node.data, choice):
					bt_probs[n] = {choice_outcome: (node_to_s[node.transitions[choice_outcome][0]],
												choice_prob) for choice_outcome, choice_prob in node.data.options()}

			for e, n in bt_req.items():
				if not relevant_events[e] and len(n) > 0:
					relevant_events[e] = True
			for e, n in bt_block.items():
				if not relevant_events[e] and len(n) > 0:
					relevant_events[e] = True

			return bt_req, bt_block, bt_trans, bt_probs, relevant_events

		def format_bt_module(name, event_names, bt_states):
			bt_req, bt_block, bt_trans, bt_probs, relevant_events = map_bt_states(event_names, bt_states)
			event_names = [e for e in event_names if relevant_events[e]]

			module_template = '\nmodule {}\n\t{}\n\n\t{}\nendmodule\n'
			state_template = "formula {}_{}_{} = {};"
			state_name = f's_{name}'
			state_init = f'{state_name}: [0..{len(bt_states)-1}] init 0;'
			event_transition = '[{}] ({}={}) -> 1: ({}\'={});'
			prob_transition = '[] ({}={}) -> {};'
			prob_format = '{}: ({}\'={})'

			req = [state_template.format(name, "req", e,
					' | '.join([('({}={})').format(state_name, n)
					for n in bt_req[e]]) if len(bt_req[e]) > 0 else 'false')
				for e in event_names]

			block = [state_template.format(name, "block", e,
					' | '.join([('({}={})').format(state_name, n)
					for n in bt_block[e]]) if len(bt_block[e]) > 0 else 'false')
				for e in event_names]

			transitions = []
			for n, tr in bt_trans.items():
				string_tr = [event_transition.format(e, state_name,
								n, state_name, s_tag) for e, s_tag in tr.items()
								if e in event_names]
				transitions.append('\n\t'.join(string_tr))
			
			probabilities = []
			for n, c in bt_probs.items():
				string_prob = [prob_format.format(p, state_name, next_state)
								for next_state, p in c.values()]
				probabilities.append(prob_transition.format(state_name, n,
									' + '.join(string_prob)))

			module = ''
			module += '\n\n'.join(
				['\n'.join(sec) for sec in [req,block]])

			module += module_template.format(name,
									state_init, '\n\t\n\t'.join(transitions + probabilities))

			return module, event_names

		text, bt_events = zip(*[format_bt_module(bt_name, event_names,
								bp_states[bt_name]) for bt_name in self.bt_names])
		content = '\n\n'.join([t for t in text])
		
		# header regulating which events are enabled + main module
		
		req = [rule_template.format(e, "req",
				' | '.join([bt_condition.format(bt,'req',e,'true')
				for i, bt in enumerate(self.bt_names) if e in bt_events[i]]))
			for e in event_names]

		block = [rule_template.format(e, "block",
				' | '.join([bt_condition.format(bt,'block',e,'true')
				for i, bt in enumerate(self.bt_names) if e in bt_events[i]]))
			for e in event_names]

		enable = [rule_template.format(e, "enabled",
				' & '.join([f'({e}_req=true)',
							f'({e}_block=false)']))
			for e in event_names]

		labels = ["label \"{}\" = ({}_enabled=true);".format(e, e)
					for e in event_names]
		
		event_transition = '[{}] ({}_enabled=true) -> 1: (event\'={});'
		guards = '\n\t'.join([event_transition.format(e, e, i)
						for i, e in enumerate(event_names)])
		module_main = f'\nmodule main\n\tevent: [-1..{len(event_names)}] init -1;'+\
						f'\n\t{guards}\nendmodule\n'

		header += '\n\n'.join(
			['\n'.join(sec) for sec in [req,block,enable,
				labels]])
		
		header += module_main
		header += '\n//-----------------------\n\n'

		if output_file:
			with open(output_file, "w") as f:
				f.write(header + content)
		return header + content

