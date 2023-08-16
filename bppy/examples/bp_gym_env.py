import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import b_thread
from bppy.gym import *
import numpy as np

@b_thread
def add_hot():
    for i in range(5):
        yield {request: bp.BEvent("HOT"), localReward: -0.01}
    yield {waitFor: bp.All(), localReward: 1}

@b_thread
def add_cold():
    for i in range(5):
        yield {request: bp.BEvent("COLD")}


@b_thread
def control():
    while True:
        yield {waitFor: bp.BEvent("HOT")}
        yield {waitFor: bp.BEvent("COLD"), block: bp.BEvent("HOT")}


def init_bprogram():
    return bp.BProgram(bthreads=[add_hot(), add_cold(), control()],
                       event_selection_strategy=bp.SimpleEventSelectionStrategy())


if __name__ == '__main__':
    event_list = [bp.BEvent("HOT"), bp.BEvent("COLD")]
    env = BPEnv(bprogram_generator=init_bprogram,
                event_list=event_list,
                observation_space=SimpleBPObservationSpace(init_bprogram, event_list),
                reward_function=lambda rewards: sum(filter(None, rewards)))
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

