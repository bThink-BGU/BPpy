Learning a BProgram as a gym environment
++++++++++++++++++++++++++++++++++++++++

This example demonstrates how to learn a BProgram as a gym environment, using the package's extension to the OpenAI gym.
In this extension, we have incorporated a :code:`localReward` parameter into the yield statement, reflecting the system's preferences.
The :class:`BPEnv <bppy.gym.bp_env.BPEnv>` class implementation requires a b-program generator - a function that creates a new instance of the b-program and the list of program events.
The default observation space for the b-program within :class:`BPEnv <bppy.gym.bp_env.BPEnv>` is represented as a Cartesian product of the b-thread's execution points, classified as multi-discrete.
For developers seeking to tailor observation space to specific needs, alternative implementations can be created by extending the abstract class :class:`BPObservationSpace <bppy.gym.bp_observation_space.BPObservationSpace>`, which includes access to both the b-thread's execution point and its local variables.
The Reward computation at each state is determined through a function that receives the reward statements from all b-threads. The default approach calculates the total reward at each yield point by summing the individual rewards from all active b-threads.

.. literalinclude :: ../../examples/bp_gym_env.py

Note that not all events are necessarily considered actions.
This distinction enables discernment between controllable and uncontrollable program behaviors.
For instance, the following b-program implements the `frozen lake environment <https://gymnasium.farama.org/environments/toy_text/frozen_lake>`_:

.. literalinclude :: ../../examples/frozen_lake_env.py
