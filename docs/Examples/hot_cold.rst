Hot Cold
+++++++++++

This program defines three b-threads that interact to control the mixing of hot and cold water from respective taps.
:code:`add_hot` and :code:`add_cold` are b-threads that request the addition of three hot and cold water portions respectively.
To control the temperature, the :code:`control_temp` b-thread continuously blocks the previously selected event (returned from the :code:`yield` command).
I continuously progresses as it waits for all events using the :class:`All <bppy.model.event_set.All>` event set.

.. literalinclude :: ../../examples/hot_cold_all.py