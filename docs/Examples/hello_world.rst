Hello World
+++++++++++

A traditional "Hello World" example in BP.
The program defines two b-threads that request specific events, "Hello" and "World".
A :code:`BProgram` is created with the two b-threads, a simple event selection strategy, and a listener that prints the selected events
The exact order and selection of the events can vary based on the underlying event selection strategy.

.. literalinclude :: ../../examples/hello_world.py