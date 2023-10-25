import stormpy

path = './monty_out.pm'
prism_program = stormpy.parse_prism_program(path)
model = stormpy.build_model(prism_program)

for state in model.states:
	for action in state.actions:
		for transition in action.transitions:
			print("From state {}, with probability {}, go to state {}".format(state, transition.value(), transition.column))