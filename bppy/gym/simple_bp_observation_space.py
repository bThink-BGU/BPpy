from bppy.gym.bp_observation_space import BPObservationSpace
import numpy as np
from bppy.utils.dfs import DFSBThread


class SimpleBPObservationSpace(BPObservationSpace):
    """
    Defines a simple observation space for BPrograms that inherit from
    :class:`BPObservationSpace <bppy.gym.bp_observation_space.BPObservationSpace>`. This class is responsible for
    mapping the state of the BProgram's bthreads to a Gym-compatible observation space.

    Attributes
    ----------
    bprogram_generator : callable
        A function that generates an instance of the BProgram.
    event_list : list
        A list of possible events in the BProgram.

    """
    def __init__(self, bprogram_generator, event_list, dtype=np.int64, seed=None):
        """
        Initializes the :class:`SimpleBPObservationSpace <bppy.gym.simaple_bp_observation_space.SimpleBPObservationSpace>`.

        Parameters
        ----------
        bprogram_generator : callable
            A function that generates an instance of the BProgram.
        event_list : list
            A list of possible events in the BProgram.
        dtype : data-type, optional
            Data type for the observation space, defaults to `np.int64`.
        seed : `int` or `None`, optional
            Seed for the random number generator, defaults to None.
        """
        self.bprogram_generator = bprogram_generator
        self.event_list = event_list
        self.mapper = self.compute_bthread_state_space()
        self.bt_state_sizes = np.asarray([len(self.mapper[x]) for x in self.mapper], dtype=dtype)
        super(SimpleBPObservationSpace, self).__init__(self.bt_state_sizes, dtype, seed)

    def bp_state_to_gym_space(self, bthreads_states):
        """
        Converts the state of the BProgram's bthreads to the Gym-compatible observation space.

        Parameters
        ----------
        bthreads_states : list
            A list representing the bthreads current statements.

        Returns
        -------
        gym_space : `np.ndarray`
            An array representing the Gym-compatible observation space.
        """
        return np.asarray([x.index(y) for x, y in zip(self.mapper.values(), bthreads_states)], dtype=self.dtype)

    def compute_bthread_state_space(self):
        mapper = {}
        n = len(self.bprogram_generator().bthreads)
        ess = self.bprogram_generator().event_selection_strategy
        for i in range(n):
            f = lambda: self.bprogram_generator().bthreads[i]
            dfs = DFSBThread(f, ess, self.event_list)
            init_s, visited = dfs.run()
            visited = [s.data for s in visited]
            mapper[i] = visited
        return mapper