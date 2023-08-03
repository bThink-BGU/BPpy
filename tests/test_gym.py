import unittest
from bppy import *
from bppy.gym import *
import numpy as np


class TestGym(unittest.TestCase):

    def test_env(self):
        @b_thread
        def add_hot():
            _reward = -0.1
            for _state in range(3):
                yield {request: BEvent("HOT")}
            _state = 3
            _reward = 1
            yield {request: BEvent("DONE")}

        @b_thread
        def add_cold():
            for _state in range(3):
                yield {request: BEvent("COLD")}

        @b_thread
        def control():
            while True:
                _state = 0
                yield {waitFor: BEvent("HOT")}
                _state = 1
                yield {waitFor: BEvent("COLD"), block: BEvent("HOT")}

        def init_bprogram():
            return BProgram(bthreads=[add_hot(), add_cold(), control()],
                               event_selection_strategy=SimpleEventSelectionStrategy())

        class SimpleStateSpace(BPObservationSpace):
            def __init__(self, bt_state_sizes, dtype=np.int64, seed=None):
                self.bt_state_sizes = np.asarray(bt_state_sizes, dtype=dtype)
                super(SimpleStateSpace, self).__init__(self.bt_state_sizes, dtype, seed)

            def bp_state_to_gym_space(self, bthreads_states):
                return np.asarray([s if s is not None else d - 1 for s, d in zip(bthreads_states, self.bt_state_sizes)],
                                  dtype=self.dtype)

        def reward_function(rewards):
            return sum(filter(None, rewards))

        env = BPEnv(bprogram_generator=init_bprogram,
                    event_list=[BEvent("HOT"), BEvent("COLD"), BEvent("DONE")],
                    observation_space=SimpleStateSpace([5, 4, 2]),
                    reward_function=reward_function)

        state, _ = env.reset()
        assert (state == np.asarray([0, 0, 0])).all()
        state, reward, terminated, _, info = env.step(0)
        assert (state == np.asarray([1, 0, 1])).all()