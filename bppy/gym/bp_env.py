import gymnasium as gym
from bppy.gym.bp_action_space import BPActionSpace
from bppy.gym.simple_bp_observation_space import SimpleBPObservationSpace
from bppy import SolverBasedEventSelectionStrategy


class BPEnv(gym.Env):
    """

    """
    def __init__(self, bprogram_generator, event_list, observation_space=None, reward_function=None):
        self.metadata = {}
        self.bprogram = None
        self.bprogram_generator = bprogram_generator
        self.action_space = BPActionSpace(event_list)
        self.reward_function = reward_function
        if self.reward_function is None:
            self.reward_function = lambda rewards: sum(filter(None, rewards))
        self.observation_space = observation_space
        if self.observation_space is None:
            self.observation_space = SimpleBPObservationSpace(self.bprogram_generator, event_list)
    def step(self, action):
        if self.bprogram is None:
            raise RuntimeError("You must call reset() before calling step()")
        if not self.action_space.contains(action):
            return self._state(), 0, True, None, {"message": "Last event is disabled"}
        event = self.action_space.event_list[action]
        self.bprogram.advance_bthreads(self.bprogram.tickets, event)
        done = self.bprogram.event_selection_strategy.selectable_events(self.bprogram.tickets).__len__() == 0
        return self._state(), self._reward(), done, None, {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)
        self.bprogram = self.bprogram_generator()
        if isinstance(self.bprogram.event_selection_strategy, SolverBasedEventSelectionStrategy):
            raise NotImplementedError("SolverBasedEventSelectionStrategy is currently not supported")
        self.action_space.bprogram = self.bprogram
        self.bprogram.setup()
        return self.observation_space.bp_state_to_gym_space(self._bthreads_states()), {}

    def render(self, mode="human"):
        raise NotImplementedError()

    def close(self):
        self.bprogram = None

    def _bthreads_states(self):
        return [dict([k, v] for k, v in statement.items() if k != "bt") for statement in self.bprogram.tickets]

    def _state(self):
        return self.observation_space.bp_state_to_gym_space(self._bthreads_states())

    def _bthreads_rewards(self):
        return [x.get("reward") for x in self.bprogram.tickets]

    def _reward(self):
        return self.reward_function(self._bthreads_rewards())