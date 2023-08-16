Dynamically Adding b-threads
++++++++++++++++++++++++++++

This example shows how to dynamically add b-threads to a running system.
The :code:`control_temp` b-thread blocks the event given as an argument, then adds a new b-thread with the previously selected event and terminates.
Thus, throughout the execution of the system the program holds multiple :code:`control_temp` b-thread instances.

.. literalinclude :: ../../examples/hot_cold_dynamic.py