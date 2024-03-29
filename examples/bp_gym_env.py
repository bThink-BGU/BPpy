import bppy as bp
from bppy.gym import *
import numpy as np

@bp.thread
def add_hot():  # request hot 5 times, and specify a reward
    for i in range(5):
        yield bp.sync(request=bp.BEvent("HOT"), localReward=-0.01)
    yield bp.sync(waitFor=bp.All(), localReward=1)

@bp.thread
def add_cold():  # request cold 5 times
    for i in range(5):
        yield bp.sync(request=bp.BEvent("COLD"))


@bp.thread
def control():  # blocks HOT from occurring twice in a row
    while True:
        yield bp.sync(waitFor=bp.BEvent("HOT"))
        yield bp.sync(block=bp.BEvent("HOT"), waitFor=bp.BEvent("COLD"))


def init_bprogram():  # function to initialize the b-program with the defined b-threads
    return bp.BProgram(bthreads=[add_hot(), add_cold(), control()],
                       event_selection_strategy=bp.SimpleEventSelectionStrategy())


if __name__ == '__main__':
    # define event list
    event_list = [bp.BEvent("HOT"), bp.BEvent("COLD")]

    # initialize environment with the defined b-program generator, observation space, and reward function
    env = BPEnv(bprogram_generator=init_bprogram,
                action_list=event_list,  # all program events are considered as possible actions for the agent
                observation_space=SimpleBPObservationSpace(init_bprogram, event_list),
                reward_function=lambda rewards: sum(filter(None, rewards)))

    # reset environment and print initial state
    state, _ = env.reset()
    print(state)
    terminated = False
    while not terminated:  # loop until the environment (b-program) terminates
        action = env.action_space.sample()  # sample an action
        print(action)
        state, reward, terminated, _, info = env.step(action)  # take a step with the sampled action
        print(state, reward, terminated, info)

    # importing stable_baselines3 and initializing a PPO model
    from stable_baselines3 import PPO
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=100000)

    # running the environment again with the trained model
    state, _ = env.reset()
    print(state)
    terminated = False
    while not terminated:
        action, _states = model.predict(state)
        print(action)
        state, reward, terminated, _, info = env.step(action)
        print(state, reward, terminated, info)

