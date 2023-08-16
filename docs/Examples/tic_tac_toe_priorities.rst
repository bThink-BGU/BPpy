Using Priority Based Event Selection Strategy (Tic Tac Toe)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This example demonstrates the use of the priority based event selection strategy using a game of Tic Tac Toe, taken from
`Programming coordinated scenarios in java <https://www.wisdom.weizmann.ac.il/~dharel/papers/BPJ%20ECOOP.pdf>`_.
Each b-thread represents a rule, or a part of the tactics in the game.
The use of priorities allows the b-threads to specify cases where one requested event may be more important (or urgent) than another, emphasizing complex behavior.

.. literalinclude :: ../../examples/tic_tac_toe_priorities.py