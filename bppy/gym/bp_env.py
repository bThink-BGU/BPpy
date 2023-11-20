import gymnasium as gym
from bppy.gym.bp_action_space import BPActionSpace
from bppy.gym.simple_bp_observation_space import SimpleBPObservationSpace
from bppy import SolverBasedEventSelectionStrategy
import warnings
import random

class BPEnv(gym.Env):
    """
    Custom environment that adheres to OpenAI's Gym interface for simulating
    the behavior of a BProgram. This class is useful for integrating BPrograms
    into reinforcement learning algorithms.

    Attributes
    ----------
    action_space : :class:`BPActionSpace <bppy.gym.bp_action_space.BPActionSpace>`
        Defines the space of possible actions, i.e., events.
    observation_space : :class:`BPObservationSpace <bppy.gym.bp_observation_space.BPObservationSpace>`
        Defines the space of possible observations.
    reward_function : function, optional
        A custom function to compute the reward.

    """
    def __init__(self, bprogram_generator, action_list, observation_space=None, action_space=None, reward_function=None):
        """
        Initializes the BPEnv environment.

        Parameters
        ----------
        bprogram_generator : function
            A function that generates a new instance of the BProgram.
        action_list : list
            List of all events defined as actions.
        observation_space : :class:`BPObservationSpace <bppy.gym.bp_observation_space.BPObservationSpace>`, optional
            Space of possible observations. Defaults to
            :class:`SimpleBPObservationSpace <bppy.gym.simple_bp_observation_space.SimpleBPObservationSpace>`.
        reward_function : function, optional
            A custom function to compute the reward. If not provided, the default reward is the sum of all b-thread
            rewards.
        """
        self.metadata = {}
        self.bprogram = None
        self.bprogram_generator = bprogram_generator
        self.action_space = BPActionSpace(action_list)
        self.event_list = action_list
        self.reward_function = reward_function
        if self.reward_function is None:
            self.reward_function = lambda rewards: sum(filter(None, rewards))
        self.observation_space = observation_space
        if self.observation_space is None:
            self.observation_space = SimpleBPObservationSpace(self.bprogram_generator, action_list)

    def step(self, action):
        """
        Executes the given action and returns the resulting observation, reward, done flag, and additional information.

        Parameters
        ----------
        action : int
            An index representing the event to be executed.

        Returns
        -------
        observation : object
            The state of the environment after executing the action.
        reward : float
            The reward obtained by executing the action.
        done : bool
            Whether the episode has ended.
        truncated : bool
            Not used for this environment.
        info : dict
            Additional information for debugging.
        """
        if self.bprogram is None:
            raise RuntimeError("You must call reset() before calling step()")
        if not self.action_space.contains(action):
            return self._state(), 0, True, None, {"message": "Last event is disabled"}
        event = self.action_space.event_list[action]
        self.bprogram.advance_bthreads(self.bprogram.tickets, event)
        while not self._step_done():
            events_are_actions = [e in self.event_list for e in
                                  self.bprogram.event_selection_strategy.selectable_events(self.bprogram.tickets)]
            if any(events_are_actions):
                selectable_events = self.bprogram.event_selection_strategy.selectable_events(self.bprogram.tickets)
                if selectable_events:
                    self.bprogram.advance_bthreads(self.bprogram.tickets, random.choice(tuple(selectable_events)))
            else:
                self.bprogram.advance_bthreads(self.bprogram.tickets,
                                               self.bprogram.event_selection_strategy.select(self.bprogram.tickets))
        done = self.bprogram.event_selection_strategy.selectable_events(self.bprogram.tickets).__len__() == 0
        return self._state(), self._reward(), done, None, {}

    def reset(self, seed=None, options=None):
        """
        Resets the environment to its initial state.

        Parameters
        ----------
        seed : int, optional
            A seed for the random number generator.
        options : dict, optional
            Additional options for resetting the environment.

        Returns
        -------
        observation : object
            The initial state of the environment.
        info : dict
            Not used for this environment.
        """
        super().reset(seed=seed, options=options)
        self.bprogram = self.bprogram_generator()
        # if isinstance(self.bprogram.event_selection_strategy, SolverBasedEventSelectionStrategy):
        #     raise NotImplementedError("SolverBasedEventSelectionStrategy is currently not supported")
        self.action_space.bprogram = self.bprogram
        self.bprogram.setup()
        while not self._step_done():
            events_are_actions = [e in self.event_list for e in
                                  self.bprogram.event_selection_strategy.selectable_events(self.bprogram.tickets)]
            if any(events_are_actions):
                selectable_events = self.bprogram.event_selection_strategy.selectable_events(self.bprogram.tickets)
                if selectable_events:
                    self.bprogram.advance_bthreads(self.bprogram.tickets, random.choice(tuple(selectable_events)))
            else:
                self.bprogram.advance_bthreads(self.bprogram.tickets,
                                               self.bprogram.event_selection_strategy.select(self.bprogram.tickets))
        return self.observation_space.bp_state_to_gym_space(self._bthreads_states()), {}

    def render(self, mode="human"):
        """
        Not implemented for this environment.
        """
        raise NotImplementedError()

    def close(self):
        """
        Closes the environment, releasing any resources.
        """
        self.bprogram = None

    def get_state(self):
        """
        Returns the current state of the environment.
        """
        return self._state()

    def _bthreads_states(self):
        return [dict([k, v] for k, v in statement.items() if k != "bt") for statement in self.bprogram.tickets]

    def _state(self):
        return self.observation_space.bp_state_to_gym_space(self._bthreads_states())

    def _bthreads_rewards(self):
        return [x.get("localReward") for x in self.bprogram.tickets]

    def _reward(self):
        return self.reward_function(self._bthreads_rewards())

    def _step_done(self):
        events_are_actions = [e in self.event_list for e in self.bprogram.event_selection_strategy.selectable_events(self.bprogram.tickets)]
        if all(events_are_actions):
            return True
        else:
            if any(events_are_actions):
                warnings.warn("Some selectable events are defined in the actions list, while others are not. "
                              "The program will continue running non-action events until all selectable events "
                              "are defined in the actions list.")
            return False
