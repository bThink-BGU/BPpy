from gymnasium.spaces import Discrete
import numpy as np


class BPActionSpace(Discrete):
    """
    Defines a custom action space for BPrograms, which inherits from the Discrete space class. The actions correspond to
    selectable events in the BProgram, and this class helps to manage and validate those actions within the environment.

    Attributes
    ----------
    event_list : list
        A list of possible events in the BProgram.

    """
    def __init__(self, event_list):
        """
        Initializes the BPActionSpace.

        Parameters
        ----------
        event_list : list
            A list of possible events in the BProgram.
        """
        self.event_list = event_list
        self.bprogram = None
        Discrete.__init__(self, len(event_list))

    def sample(self):
        """
        Randomly samples an action from the set of possible actions.

        Returns
        -------
        action : int
            The index of the randomly selected action.
        """
        return self.np_random.choice(self._possible_actions())

    def contains(self, x):
        """
        Checks whether the provided value corresponds to a valid action.

        Parameters
        ----------
        x : int, np.generic, or np.ndarray
            The value to check for validity.

        Returns
        -------
        valid : bool
            True if the value is a valid action, False otherwise.
        """
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
