import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import b_thread
from bppy.gym import *
import numpy as np

@b_thread
def add_hot():
    _reward = -0.1
    for _state in range(3):
        yield {request: bp.BEvent("HOT")}
    _state = 3
    _reward = 1
    yield {request: bp.BEvent("DONE")}

@b_thread
def add_cold():
    for _state in range(3):
        yield {request: bp.BEvent("COLD")}


@b_thread
def control():
    while True:
        _state = 0
        yield {waitFor: bp.BEvent("HOT")}
        _state = 1
        yield {waitFor: bp.BEvent("COLD"), block: bp.BEvent("HOT")}


def init_bprogram():
    return bp.BProgram(bthreads=[add_hot(), add_cold(), control()],
                       event_selection_strategy=bp.SimpleEventSelectionStrategy())


class SimpleStateSpace(BPObservationSpace):
    def __init__(self, bt_state_sizes, dtype=np.int64, seed=None):
        self.bt_state_sizes = np.asarray(bt_state_sizes, dtype=dtype)
        super(SimpleStateSpace, self).__init__(self.bt_state_sizes, dtype, seed)

    def bp_state_to_gym_space(self, bthreads_states):
        return np.asarray([s if s is not None else d-1 for s, d in zip(bthreads_states, self.bt_state_sizes)], dtype=self.dtype)


def reward_function(rewards):
    return sum(filter(None, rewards))


if __name__ == '__main__':
    env = BPEnv(bprogram_generator=init_bprogram,
                event_list=[bp.BEvent("HOT"), bp.BEvent("COLD"), bp.BEvent("DONE")],
                observation_space=SimpleStateSpace([5, 4, 2]),
                reward_function=reward_function)
    state, _ = env.reset()
    print(state)
    terminated = False
    while not terminated:
        action = env.action_space.sample()
        print(action)
        state, reward, terminated, _, info = env.step(action)
        print(state, reward, terminated, info)
    from stable_baselines3 import PPO
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=100000)
    state, _ = env.reset()
    print(state)
    terminated = False
    while not terminated:
        action, _states = model.predict(state)
        print(action)
        state, reward, terminated, _, info = env.step(action)
        print(state, reward, terminated, info)




