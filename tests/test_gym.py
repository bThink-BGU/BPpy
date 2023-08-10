import unittest
from bppy import *
from bppy.gym import *
import numpy as np


class TestGym(unittest.TestCase):

    def test_env(self):
        @b_thread
        def add_hot():
            for i in range(3):
                yield {request: BEvent("HOT"), localReward: -0.1}
            yield {request: BEvent("DONE"), localReward: 1}

        @b_thread
        def add_cold():
            for i in range(3):
                yield {request: BEvent("COLD")}

        @b_thread
        def control():
            while True:
                yield {waitFor: BEvent("HOT")}
                yield {waitFor: BEvent("COLD"), block: BEvent("HOT")}

        def init_bprogram():
            return BProgram(bthreads=[add_hot(), add_cold(), control()],
                            event_selection_strategy=SimpleEventSelectionStrategy())

        env = BPEnv(bprogram_generator=init_bprogram,
                    event_list=[BEvent("HOT"), BEvent("COLD"), BEvent("DONE")])

        state, _ = env.reset()
        assert (state == np.asarray([0, 0, 0])).all()
        state, reward, terminated, _, info = env.step(0)
        assert (state == np.asarray([1, 0, 1])).all()
