Using Z3-Solver SMT based BP
++++++++++++++++++++++++++++

The following program is an adaptation of the HOT/COLD example presented in the paper `Executing Scenario-Based Specification with Dynamic Generation of Rich Events <https://www.wisdom.weizmann.ac.il/~dharel/papers/CCIS2019RichEvents.pdf>`_.
The program uses Z3-Solver to solve an solver-based BP.
In this extension, events are represented as the set of SMT variables (e.g., :code:`hot` :code:`cold` booleans and :code:`temp` real).
In each yield point, the b-threads specify requested, blocked, and waited-for constraints over the variables in the form of logical statements to be satisfied.
Upon collecting all constraints, the new execution mechanism invokes the Z3 SMT solver to find an assignment to the variables embedded in the events.
The assignment is then returned by the :code:`yield` command of the b-thread.

.. literalinclude :: ../../examples/hot_cold_smt.py