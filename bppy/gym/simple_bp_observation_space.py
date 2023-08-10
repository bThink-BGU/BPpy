from bppy.gym.bp_observation_space import BPObservationSpace
import numpy as np
from bppy.utils.dfs import DFSBThread


class SimpleBPObservationSpace(BPObservationSpace):
    def __init__(self, bprogram_generator, event_list, dtype=np.int64, seed=None):
        self.bprogram_generator = bprogram_generator
        self.event_list = event_list
        self.mapper = self.compute_bthread_state_space()
        self.bt_state_sizes = np.asarray([len(self.mapper[x]) for x in self.mapper], dtype=dtype)
        super(SimpleBPObservationSpace, self).__init__(self.bt_state_sizes, dtype, seed)

    def bp_state_to_gym_space(self, bthreads_states):
        return np.asarray([x.index(y) for x, y in zip(self.mapper.values(), bthreads_states)], dtype=self.dtype)

    def compute_bthread_state_space(self):
        mapper = {}
        n = len(self.bprogram_generator().bthreads)
        ess = self.bprogram_generator().event_selection_strategy
        for i in range(n):
            f = lambda: self.bprogram_generator().bthreads[i]
            dfs = DFSBThread(f, ess, self.event_list)
            init_s, visited = dfs.run()
            mapper[i] = visited
        return mapper