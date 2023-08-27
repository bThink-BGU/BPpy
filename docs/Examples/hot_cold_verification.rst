Verify a BProgram using Depth First Search (DFS)
++++++++++++++++++++++++++++++++++++++++++++++++

This example demonstrates how to verify a behavioral program for assertions using Depth First Search (DFS).
Currently, this class verifies only properties which can be defined using assertions in b-threads. For additional properties, or programs with large state space, use :class:`SymbolicBProgramVerifier <bppy.analysis.symbolic_bprogram_verifier.SymbolicBProgramVerifier>`.
The :class:`DFSBProgramVerifier <bppy.analysis.dfs_bprogram_verifier.DFSBProgramVerifier>` class implementation requires a b-program generator - a function that creates a new instance of the b-program and optionally a bound for the depth.

.. literalinclude :: ../../examples/hot_cold_verification.py