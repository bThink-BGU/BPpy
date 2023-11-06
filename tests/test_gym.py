import unittest
import bppy as bp
from bppy.gym import *
import numpy as np


class TestGym(unittest.TestCase):

    def test_env(self):
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

        def init_bprogram():
            return bp.BProgram(bthreads=[add_hot(), add_cold(), control()],
                            event_selection_strategy=bp.SimpleEventSelectionStrategy())

        env = BPEnv(bprogram_generator=init_bprogram,
                    action_list=[bp.BEvent("HOT"), bp.BEvent("COLD"), bp.BEvent("DONE")])

        state, _ = env.reset()
        assert (state == np.asarray([0, 0, 0])).all()
        state, reward, terminated, _, info = env.step(0)
        assert (state == np.asarray([1, 0, 1])).all()
