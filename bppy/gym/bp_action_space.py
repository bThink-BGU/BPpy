from gymnasium.spaces import Discrete
import numpy as np


class BPActionSpace(Discrete):
    """

    """
    def __init__(self, event_list):
        self.event_list = event_list
        self.bprogram = None
        Discrete.__init__(self, len(event_list))

    def sample(self):
        return self.np_random.choice(self._possible_actions())

    def contains(self, x):
        if isinstance(x, int):
            as_int = x
        elif isinstance(x, (np.generic, np.ndarray)) and (x.dtype.char in np.typecodes['AllInteger'] and x.shape == ()):
            as_int = int(x)
        else:
            return False
        return as_int in self._possible_actions()

    def __repr__(self):
        return "BPActionSpace(%d)" % self.n

    def __eq__(self, other):
        return isinstance(other, BPActionSpace) and self.bprogram == other.bprogram and self.event_list == other.event_list

    def _possible_actions(self):
        possible_events = self.bprogram.event_selection_strategy.selectable_events(self.bprogram.tickets)
        return [k for k, v in enumerate(self.event_list) if v in possible_events]
