Using External Events
+++++++++++++++++++++

This example shows how external events can be added to the program.
Each program contains a queue of external events, which can be added using the :code:`enqueue_external_event` method.
Once no internal events can be selected, the selected event will be the first external event in the queue.


.. literalinclude :: ../../examples/external_events.py