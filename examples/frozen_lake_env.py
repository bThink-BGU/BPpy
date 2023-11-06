import bppy as bp
from bppy.gym import *
import numpy as np

ROWS = 4
COLS = 4

# defining the agent actions
agent_actions = [bp.BEvent("LEFT"), bp.BEvent("RIGHT"), bp.BEvent("UP"), bp.BEvent("DOWN")]

# defining the internal events for the environment
move_event = bp.EventSet(lambda e: e.name.startswith("Move"))


class Move(bp.BEvent):
    def __init__(self, i, j):
        super().__init__("Move", {"i": i, "j": j})


# b-thread for cells in the environment, triggered when the agent moving to this cell. The b-thread than requests to
# move to the intended direction or a perpendicular direction randomly
@bp.thread
def cell(i, j):
    while True:
        yield bp.sync(waitFor=Move(i, j))
        e = yield bp.sync(waitFor=agent_actions)
        actions_and_opposite_moves = {"LEFT": Move(i, j+1),"RIGHT": Move(i, j-1),"UP": Move(i+1, j),"DOWN": Move(i-1, j)}
        # remove the opposite move to the action
        actions_and_opposite_moves.pop(e.name)
        possible_moves = list(actions_and_opposite_moves.values())
        yield bp.sync(request=possible_moves, block=agent_actions)


# b-thread for hole locations in the environment, representing terminal states
@bp.thread
def hole(i, j):
    yield bp.sync(waitFor=Move(i, j))
    yield bp.sync(block=bp.All())  # reached hole terminate the program with a reward of 0


# b-thread representing wall locations, blocking moves to this wall
@bp.thread
def wall(i, j):  # block moves to this wall
    yield bp.sync(block=Move(i, j))


# b-thread for the start of the environment run, triggering the initial location of the agent
@bp.thread
def start():
    yield bp.sync(request=Move(0, 0), block=agent_actions)


# b-thread representing the goal of the environment, providing a terminal state with reward 1
@bp.thread
def goal():
    yield bp.sync(waitFor=Move(ROWS-1, COLS-1), localReward=0)
    yield bp.sync(block=bp.All(), localReward=1)  # reached goal - terminate the program with a reward of 1


# b-thread for the agent, requesting actions based on the current location
@bp.thread
def agent():
    while True:
        e = yield bp.sync(waitFor=move_event)
        current_location = (e.data["i"], e.data["j"])
        yield bp.sync(request=agent_actions)


# function to initialize the b-program with the defined b-threads
def init_bprogram():
    """
    returning an instance for the standard 4x4 frozen lake environment:
        ["SFFF",
         "FHFH",
         "FFFH",
         "HFFG"]
    """
    holes_locations = [(1, 1), (1, 3), (2, 3), (3, 0)]
    return bp.BProgram(bthreads=[start(), agent(), goal()] +
                                [hole(i, j) if (i, j) in holes_locations else cell(i, j) for i in range(ROWS) for j in range(COLS)] +
                                [wall(-1, j) for j in range(COLS)] +
                                [wall(ROWS, j) for j in range(COLS)] +
                                [wall(i, -1) for i in range(ROWS)] +
                                [wall(i, COLS) for i in range(ROWS)],
                       event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                       listener=bp.PrintBProgramRunnerListener())

# listing all possible events in the b-program
all_events = [Move(i, j) for i in range(-1, ROWS+1) for j in range(-1, COLS+1)] + agent_actions + [bp.BEvent("HOLE"), bp.BEvent("GOAL")]


# defining the observation space for the environment based on the current_location variable of the agent b-thread
class FrozenLakeObservationSpace(BPObservationSpace):
    def __init__(self, dim):
        super().__init__([dim], np.int64, None)
    def bp_state_to_gym_space(self, bthreads_states):
        agent_bthread_statement = [x for x in bthreads_states if "current_location" in x.get("locals", {})][0]
        current_location = agent_bthread_statement["locals"]["current_location"]
        return np.asarray([current_location[0]*COLS + current_location[1]], dtype=self.dtype)


# initialize environment with the defined b-program generator, observation space, and reward function
env = BPEnv(bprogram_generator=init_bprogram,
            action_list=agent_actions,  # all program events are considered as possible actions for the agent
            observation_space=FrozenLakeObservationSpace(ROWS*COLS),
            reward_function=lambda rewards: sum(filter(None, rewards)))

# reset environment and print initial state
state, _ = env.reset()
print(state)
terminated = False
while not terminated:  # loop until the environment (b-program) terminates
    action_id = env.action_space.sample()  # sample an action
    state, reward, terminated, _, info = env.step(action_id)  # take a step with the sampled action
    print(agent_actions[action_id].name, state, reward, terminated, info)


# importing stable_baselines3 and initializing a PPO model
from stable_baselines3 import PPO
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100000)

# running the environment again with the trained model
state, _ = env.reset()
print(state)
terminated = False
while not terminated:
    action_id, _states = model.predict(state)
    state, reward, terminated, _, info = env.step(action_id)
    print(agent_actions[action_id].name, state, reward, terminated, info)
