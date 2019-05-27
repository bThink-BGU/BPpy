import gym
from gym import error, spaces, utils
from gym.utils import seeding
from z3 import *
from random import randint, choice
from mde import mde_return_variables as mrv
from mde.smt_variables import *
import numpy as np


class BPEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.bprogram = None
        self.np_random = None
        self.last_event = None
        self.listener = None

    def step(self, action):
        self.last_event = self.bprogram.event_selection_strategy.select(self.bprogram.tickets, action)
        #print(self.last_event)
        cur_reward = float(self.last_event[rewardReal].as_string())
        if self.last_event is None:
            #print("done", cur_reward)
            return None, cur_reward, True, {}
        else:
            if self.listener:
                interrupted = self.listener.event_selected(b_program=self.bprogram, event=self.last_event)
            self.bprogram.advance_bthreads(self.last_event)
            for _ in range(5):  # TODO: change
                self.last_event = self.bprogram.next_event()
                if self.listener:
                    interrupted = self.listener.event_selected(b_program=self.bprogram, event=self.last_event)
                self.bprogram.advance_bthreads(self.last_event)
            state = [mrv.getSuctionReal, mrv.GPSRealx, mrv.GPSRealy, mrv.ballGPSRealx, mrv.ballGPSRealy, mrv.getCompassReal]
            #print(state, cur_reward)
            return np.array(state), cur_reward, False, {}

    def reset(self):
        self.last_event = None
        if self.listener:
            self.listener.starting(b_program=self.bprogram)

        self.bprogram.setup()
        for _ in range(5):  # TODO: change
            self.last_event = self.bprogram.next_event()
            if self.listener:
                interrupted = self.listener.event_selected(b_program=self.bprogram, event=self.last_event)
            self.bprogram.advance_bthreads(self.last_event)
        state = [mrv.getSuctionReal, mrv.GPSRealx, mrv.GPSRealy, mrv.ballGPSRealx, mrv.ballGPSRealy, mrv.getCompassReal]
        return np.array(state)

    def render(self, mode='human', close=False):
        raise NotImplementedError

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def set_bprogram(self, bprogram):
        self.bprogram = bprogram

    def set_listener(self, listener):
        self.listener = listener

# import sys
# sys.path.append("/Users/tomyaacov/Desktop/university/thesis/BPpy")
# from model.bprogram import Bprogram
# from execution.listeners.print_b_program_runner_listener import PrintBProgramRunnerListener
# from model.event_selection.smt_event_selection_strategy import SMTEventSelectionStrategy
# from model.event_selection.simple_event_selection_strategy import SimpleEventSelectionStrategy
#
# if __name__ == "__main__":
#     bprogram =Bprogram(source_name="rumba_discrete",
#                        event_selection_strategy=SMTEventSelectionStrategy(),
#                        listener=PrintBProgramRunnerListener())
#     env = BPEnv()
#     env.set_bprogram(bprogram)
#     observation = env.reset()
#     for _ in range(100):
#         # env.render()
#         action = choice([10,11,20])
#         observation, reward, done, info = env.step(action)
#         if done:
#             # observation = env.reset()
#             break
#     env.close()